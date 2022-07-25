defmodule Indicator.Application do
  use Application

  @impl true
  def start(_type, _args) do
    children = [
#      Rabbit
      Indicator.Repo
    ]

    opts = [strategy: :one_for_one, name: Indicator.Supervisor]
    Supervisor.start_link(children, opts)
  end

end
