default:
    @just --list

install:
    @pnpm install

dev:
    @pnpm dev

build:
    @pnpm build

preview:
    @pnpm preview

format:
    @pnpm format

lint:
    @pnpm lint:fix

typecheck:
    @pnpm typecheck

ci: format lint typecheck

clean:
    @rm -rf node_modules dist .astro

deploy: build
    wrangler pages deploy dist --project-name=spaceos
