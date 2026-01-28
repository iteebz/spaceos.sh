import react from '@astrojs/react'
import tailwind from '@astrojs/tailwind'
import { defineConfig } from 'astro/config'

export default defineConfig({
	site: 'https://space-os.dev',
	integrations: [react(), tailwind()],
	server: { port: 3227 },
})
