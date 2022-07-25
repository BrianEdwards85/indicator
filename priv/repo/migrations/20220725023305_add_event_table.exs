defmodule Indicator.Repo.Migrations.AddEventTable do
  use Ecto.Migration

  def change do
    create table(:events, primary_key: false) do
      add :id,        :text,    primary_key: true, default: fragment("uuid_generate_v4()")
      add :device_id, references(:devices, type: :text), null: false
      add :payload,   :jsonb,   null: false
      timestamps default: fragment("now()")
    end

    create table(:reading_types, primary_key: false) do
      add :id,          :text,    primary_key: true, default: fragment("uuid_generate_v4()")
      add :description, :text,    null: false
      timestamps default: fragment("now()")
    end

    create table(:readings, primary_key: false) do
      add :id,            :text,    primary_key: true, default: fragment("uuid_generate_v4()")
      add :event_id,      references(:events, type: :text), null: false
      add :event_type_id, references(:reading_types, type: :text), null: false
      add :val,           :jsonb,   null: false
      timestamps default: fragment("now()")
    end

    create table(:device_state, primary_key: false) do
      add :id,        :text,    primary_key: true, default: fragment("uuid_generate_v4()")
      add :device_id, references(:devices, type: :text), null: false
      add :event_id,  references(:events, type: :text), null: false
      add :state,     :text,    null: false
      timestamps default: fragment("now()")
    end
  end
end
