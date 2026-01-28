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

ci:
    @pnpm format
    @pnpm lint:fix
    @pnpm typecheck

clean:
    @rm -rf node_modules dist .astro
