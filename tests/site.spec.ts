import { test, expect } from 'playwright/test'

test.describe('Landing Page', () => {
  test('renders hero title', async ({ page }) => {
    await page.goto('/')
    await expect(page.locator('h2').first()).toContainText('space')
  })

  test('renders stats section', async ({ page }) => {
    await page.goto('/')
    await expect(page.locator('#live-stats')).toBeVisible()
  })

  test('renders navigation links', async ({ page }) => {
    await page.goto('/')
    await expect(page.locator('a[href="/docs/thesis"]')).toBeVisible()
    await expect(page.locator('a[href="/docs/philosophy"]')).toBeVisible()
    await expect(page.locator('a[href="/swarm/papers"]')).toBeVisible()
  })
})

test.describe('Docs Pages', () => {
  test('thesis page renders', async ({ page }) => {
    await page.goto('/docs/thesis')
    await expect(page).toHaveTitle(/thesis/i)
  })

  test('philosophy page renders', async ({ page }) => {
    await page.goto('/docs/philosophy')
    await expect(page).toHaveTitle(/philosophy/i)
  })

  test('walkthrough page renders', async ({ page }) => {
    await page.goto('/docs/walkthrough')
    await expect(page).toHaveTitle(/walkthrough|how it works/i)
  })
})

test.describe('Swarm Pages', () => {
  test('papers page renders', async ({ page }) => {
    await page.goto('/swarm/papers')
    await expect(page.locator('h1, h2').first()).toBeVisible()
  })

  test('findings index renders', async ({ page }) => {
    await page.goto('/swarm/findings')
    await expect(page.locator('h1, h2').first()).toBeVisible()
  })

  test('live metrics page renders', async ({ page }) => {
    await page.goto('/swarm/live')
    await expect(page.locator('h1, h2').first()).toBeVisible()
  })
})

test.describe('API', () => {
  test('stats.json returns data', async ({ request }) => {
    const res = await request.get('/stats.json')
    expect(res.status()).toBe(200)
    const data = await res.json()
    expect(data).toHaveProperty('days_active')
  })
})
