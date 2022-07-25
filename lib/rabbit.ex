defmodule Rabbit do
  use GenServer
  require Logger

  @restart_delay 2000 # 2 seconds

  def start_link(_args) do
    config = Application.get_env(:grandfather, Rabbit)
    GenServer.start(__MODULE__, config, name: __MODULE__)
  end

  @impl true
  def init(config) do
    Application.ensure_started(:amqp)
    Process.flag(:trap_exit, true)
    send(self(), :connect)
    {:ok, %{config: config}}
  end

  @impl true
  def handle_info(:connect, %{config: config}) do
    case AMQP.Connection.open(config) do
      {:ok, connection} ->
        Process.link(connection.pid)
        {:ok, channel} = AMQP.Channel.open(connection)
        {:noreply, %{connection: connection, channel: channel, config: config}}
      {:error, :econnrefused} ->
        Logger.error("amqp transport failed with connection refused")
        Process.send_after(self(), :connect, @restart_delay)
        {:noreply, %{config: config}}
    end
  end

  @impl true
  def handle_info({:EXIT, pid, reason}, %{config: config}) do
    Logger.error("amqp transport failed with #{inspect(reason)}")
    Process.unlink(pid)
    Process.send_after(self(), :connect, @restart_delay)
    {:noreply, %{config: config}}
  end


  def publish(topic, message) do
    GenServer.call(__MODULE__, {:publish, topic, message})
  end

  def subscribe(topics, consumer \\ nil)
  def subscribe(topics, consumer) when is_list(topics) do
    GenServer.call(__MODULE__, {:subscribe, topics, consumer})
  end

  def subscribe(topic, consumer) when is_bitstring(topic), do: subscribe([topic], consumer)



  @impl true
  def handle_call({:publish, topic, message}, _from, %{channel: channel} = state) do
    r = AMQP.Basic.publish(channel, "amq.topic", topic, message)
    {:reply, r, state}
  end

  def handle_call({:subscribe, topics, consumer}, from, %{connection: connection} = state) do
    {:ok, channel} = AMQP.Channel.open(connection)
    {:ok, %{queue: queue}} = AMQP.Queue.declare(channel,"", auto_delete: true, exclusive: true )
    for topic <- topics, do: AMQP.Queue.bind(channel, queue, "amq.topic", routing_key: topic)

    consumer_pid = consumer || from

    pid = spawn(fn -> message_consumer(channel, consumer_pid) end)

    {:ok, consumer_tag} = AMQP.Basic.consume(channel, queue, pid)

    unsub = fn -> AMQP.Basic.cancel(channel, consumer_tag) end
    {:reply, unsub, state}
  end

  defp message_consumer(channel, from) do
    receive do
      {:basic_deliver, payload, meta} ->
        send(from, {:message, Map.put(meta, :message, payload)})
        message_consumer(channel, from)
      {:basic_cancel, _} ->
        AMQP.Channel.close(channel)
        send(from, {:cancel})
      {:basic_cancel_ok, _} ->
        AMQP.Channel.close(channel)
        send(from, {:cancel})
    end
  end

  defp debug_consumer() do
      receive do
        {:message, payload} ->
          IO.puts("Message: #{inspect(payload)}")
          debug_consumer()
        {:cancel} -> IO.puts("Done")
      end
  end

  def sub(topics) do
    pid = spawn(&debug_consumer/0)
    subscribe(topics, pid)
  end
end
