defmodule Indicator.Repo.Device do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :string, []}
  schema "devices" do
    field :addr, :string
    field :name, :string
    field :enabled, :boolean
    timestamps()
  end

    @doc false
    def changeset(device, attrs) do
      device
      |> cast(attrs, [:id, :addr, :name, :enabled])
      |> validate_required([:id, :addr, :name])
    end
end
