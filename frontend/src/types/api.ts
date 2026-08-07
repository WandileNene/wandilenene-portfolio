// ─── API Response Types ──────────────────────────────────────────────────────
// These mirror the Pydantic response schemas from backend/app/schemas.py exactly.

export interface Profile {
  id: number
  full_name: string
  title: string
  tagline: string | null
  bio: string | null
  profile_image: string | null
  email: string
  phone: string | null
  location: string | null
  github_url: string | null
  linkedin_url: string | null
  twitter_url: string | null
  created_at: string
  updated_at: string
}

export interface Education {
  id: number
  degree: string
  field_of_study: string
  institution: string
  location: string | null
  start_date: string
  end_date: string | null
  grade: string | null
  description: string | null
  is_current: boolean
  order: number
  created_at: string
  updated_at: string
}

export interface Experience {
  id: number
  title: string
  company: string
  location: string | null
  employment_type: string | null
  start_date: string
  end_date: string | null
  is_current: boolean
  description: string | null
  responsibilities: string[] | null
  technologies: string[] | null
  order: number
  created_at: string
  updated_at: string
}

export interface Skill {
  id: number
  name: string
  proficiency: number
  icon: string | null
  order?: number
}

export interface SkillsByCategory {
  [category: string]: Skill[]
}

export interface Certification {
  id: number
  name: string
  issuing_organization: string
  issue_date: string
  expiry_date: string | null
  credential_id: string | null
  credential_url: string | null
  description: string | null
  order: number
  created_at: string
  updated_at: string
}

export interface Project {
  id: number
  name: string
  slug: string
  short_description: string
  description: string | null
  technologies: string[] | null
  features: string[] | null
  github_url: string | null
  demo_url: string | null
  image_url: string | null
  status: 'completed' | 'in-progress' | 'archived'
  is_featured: boolean
  order: number
  created_at: string
  updated_at: string
}

export interface Achievement {
  id: number
  title: string
  issuer: string
  date: string
  description: string | null
  icon: string | null
  order: number
  created_at: string
  updated_at: string
}

export interface Resume {
  id: number
  filename: string
  original_filename: string
  file_size: number
  content_type: string
  version: string | null
  description: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface PortfolioStats {
  total_projects: number
  featured_projects: number
  total_skills: number
  skill_categories: number
  total_certifications: number
  total_achievements: number
  years_of_experience: number
}

export interface PortfolioSummary {
  profile: Profile | null
  education: Education[]
  experience: Experience[]
  skills: SkillsByCategory
  certifications: Certification[]
  projects: Project[]
  achievements: Achievement[]
  stats: PortfolioStats
}

export interface ContactMessagePayload {
  name: string
  email: string
  subject?: string
  message: string
}
