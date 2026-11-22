import type { Template } from '../types/template'
import { api } from './client'

export async function fetchTemplates(): Promise<Template[]> {
  return (await api.get<Template[]>('/templates')).data
}
