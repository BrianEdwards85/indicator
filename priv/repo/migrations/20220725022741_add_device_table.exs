defmodule Indicator.Repo.Migrations.AddDeviceTable do
  use Ecto.Migration

  def change do
    create table(:devices, primary_key: false) do
      add :id,      :text,    primary_key: true, default: fragment("uuid_generate_v4()")
      add :addr,    :text,    null: false
      add :name,    :text,    null: false
      add :enabled, :boolean, null: false, default: true
      timestamps default: fragment("now()")
    end
  end
end
