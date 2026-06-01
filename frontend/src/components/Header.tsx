export default function Header() {
  return (
    <header className="border-b border-border bg-panel/60 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="grid h-9 w-9 place-items-center rounded-lg bg-gradient-to-br from-accent2 to-accent text-ink font-black">
            AF
          </div>
          <div>
            <div className="text-base font-semibold">Award Finder</div>
            <div className="text-xs text-muted">
              Free transatlantic award search across loyalty programs
            </div>
          </div>
        </div>
        <a
          href="https://github.com"
          className="text-xs text-muted hover:text-slate-200"
          target="_blank"
          rel="noreferrer"
        >
          GitHub
        </a>
      </div>
    </header>
  );
}
