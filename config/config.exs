import Config

config :indicator, ecto_repos: [Indicator.Repo]

config :indicator, Indicator.Repo,
  database: "indicator_dev",
  username: "indicator_user",
  password: "indicator_user",
  hostname: "192.168.104.11"
