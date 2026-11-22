export type Template = {
  id: number
  name: string
  subject: string
  body: string
  category: string | null
  variables: string[]
  is_active: boolean
  created_at: string
  updated_at: string
}
