import { EnvelopeIcon } from '@heroicons/react/24/outline'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { api } from '../api/client'

type Health = { status: string }

export default function HomePage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['health'],
    queryFn: async () => (await api.get<Health>('/health')).data,
  })

  return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="bg-white rounded-xl shadow p-8 max-w-md w-full text-center space-y-4">
        <EnvelopeIcon className="h-12 w-12 mx-auto text-indigo-600" />
        <h1 className="text-2xl font-bold text-gray-900">Email Generator</h1>
        <p className="text-gray-600">
          Backend :{' '}
          {isLoading ? (
            <span className="text-gray-400">vérification…</span>
          ) : isError ? (
            <span className="text-red-600 font-medium">injoignable</span>
          ) : (
            <span className="text-green-600 font-medium">{data?.status}</span>
          )}
        </p>
        <Link to="/templates" className="inline-block text-indigo-600 font-medium hover:underline">
          Voir les templates →
        </Link>
      </div>
    </main>
  )
}
