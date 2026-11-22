import { DocumentTextIcon, FolderIcon } from '@heroicons/react/24/outline'
import { useQuery } from '@tanstack/react-query'
import { useMemo } from 'react'
import { Link } from 'react-router-dom'
import { fetchTemplates } from '../api/templates'
import type { Template } from '../types/template'

const UNCATEGORIZED = 'Sans catégorie'

function groupByCategory(templates: Template[]): [string, Template[]][] {
  const groups = new Map<string, Template[]>()
  for (const t of templates) {
    const key = t.category?.trim() || UNCATEGORIZED
    const list = groups.get(key)
    if (list) list.push(t)
    else groups.set(key, [t])
  }
  return [...groups.entries()].sort(([a], [b]) => {
    if (a === UNCATEGORIZED) return 1
    if (b === UNCATEGORIZED) return -1
    return a.localeCompare(b, 'fr')
  })
}

function TemplateCard({ template }: { template: Template }) {
  return (
    <li className="bg-white rounded-lg shadow-sm ring-1 ring-gray-200 p-4 space-y-2">
      <div className="flex items-start justify-between gap-2">
        <h3 className="font-semibold text-gray-900 flex items-center gap-2">
          <DocumentTextIcon className="h-5 w-5 text-indigo-600 shrink-0" />
          {template.name}
        </h3>
        {!template.is_active && (
          <span className="text-xs font-medium rounded-full bg-gray-100 text-gray-600 px-2 py-0.5">
            Inactif
          </span>
        )}
      </div>
      <p className="text-sm text-gray-700">
        <span className="text-gray-500">Objet :</span> {template.subject}
      </p>
      <p className="text-sm text-gray-500 line-clamp-3 whitespace-pre-line">{template.body}</p>
      {template.variables.length > 0 && (
        <div className="flex flex-wrap gap-1 pt-1">
          {template.variables.map((v) => (
            <span
              key={String(v)}
              className="text-xs font-mono rounded bg-indigo-50 text-indigo-700 px-1.5 py-0.5"
            >
              {`{{${v}}}`}
            </span>
          ))}
        </div>
      )}
    </li>
  )
}

export default function TemplatesPage() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['templates'],
    queryFn: fetchTemplates,
  })

  const groups = useMemo(() => groupByCategory(data ?? []), [data])

  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-5xl mx-auto space-y-8">
        <header className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">Templates</h1>
          <Link to="/" className="text-sm text-indigo-600 hover:underline">
            Accueil
          </Link>
        </header>

        {isLoading && <p className="text-gray-500">Chargement…</p>}

        {isError && (
          <p className="text-red-600">
            Impossible de charger les templates : {(error as Error).message}
          </p>
        )}

        {data && data.length === 0 && (
          <p className="text-gray-500">Aucun template pour le moment.</p>
        )}

        {groups.map(([category, templates]) => (
          <section key={category} className="space-y-3">
            <h2 className="flex items-center gap-2 text-lg font-semibold text-gray-800">
              <FolderIcon className="h-5 w-5 text-gray-400" />
              {category}
              <span className="text-sm font-normal text-gray-500">({templates.length})</span>
            </h2>
            <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {templates.map((t) => (
                <TemplateCard key={t.id} template={t} />
              ))}
            </ul>
          </section>
        ))}
      </div>
    </main>
  )
}
