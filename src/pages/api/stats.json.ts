import type { APIRoute } from 'astro'
import stats from '../../../public/stats.json'

export const GET: APIRoute = () => {
	return new Response(JSON.stringify(stats), {
		status: 200,
		headers: {
			'Content-Type': 'application/json',
			'Cache-Control': 'public, max-age=60',
			'Access-Control-Allow-Origin': '*',
		},
	})
}
