defmodule Indicator.Repo.Devices do
  import Ecto.Query, warn: false
  alias Indicator.Repo
  alias Indicator.Repo.Device

  def list_devices(), do: Repo.all(Device)
  def get_device(id), do: Repo.get(Device, id)

  def add_device(attrs \\ %{}) do
    id = Ecto.UUID.generate()
    %Device{id: id}
    |> Device.changeset(attrs)
    |> Repo.insert()
  end

  def update_device(%{:id => id} = attrs) do
    get_device(id)
    |> Device.changeset(attrs)
    |> Repo.update()
  end
end
