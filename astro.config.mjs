import mdx from '@astrojs/mdx'
import react from '@astrojs/react'
import tailwind from '@astrojs/tailwind'
import { defineConfig } from 'astro/config'

export default defineConfig({
	site: 'https://spaceos.sh',
	integrations: [react(), tailwind(), mdx()],
	server: { port: 3227 },
})
