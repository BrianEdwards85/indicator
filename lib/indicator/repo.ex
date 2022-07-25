defmodule Indicator.Repo do
  use Ecto.Repo,
    otp_app: :indicator,
    adapter: Ecto.Adapters.Postgres
end
