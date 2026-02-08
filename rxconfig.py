import reflex as rx

config = rx.Config(
	app_name="reflex_state_examples",
	plugins=[rx.plugins.TailwindV3Plugin()],
	disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
	state_auto_setters=True,
)
