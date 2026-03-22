<template>
  <header class="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-end shrink-0">
    <div class="flex items-center gap-2">
      <!-- API Docs -->
      <a
        href="http://localhost:8000/docs"
        target="_blank"
        rel="noopener noreferrer"
        class="inline-flex items-center justify-center h-8 w-8 rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-100 transition-colors"
        title="API Docs"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M8 9l-3 3 3 3M16 9l3 3-3 3M12 5l-2 14" />
        </svg>
      </a>

      <!-- Release Notes -->
      <a
        href="/CHANGELOG.md"
        target="_blank"
        rel="noopener noreferrer"
        class="inline-flex items-center justify-center h-8 w-8 rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-100 transition-colors"
        title="Release Notes"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M9 12h6M9 8h6M9 16h4M5 4h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"
          />
        </svg>
      </a>
    </div>
  </header>
</template>
