import { usePortfolio } from './hooks/usePortfolio'
import { Navbar } from './components/Navbar/Navbar'
import { Hero } from './components/Hero/Hero'
import { LoadingSpinner } from './components/shared/LoadingSpinner'
import { SectionHeader } from './components/shared/SectionHeader'
import { Badge } from './components/shared/Badge'
import './styles/global.css'

function App() {
  const { data, loading, error } = usePortfolio()

  if (loading) return <LoadingSpinner />
  if (error) return (
    <div style={{ 
      padding: '2rem', 
      textAlign: 'center', 
      minHeight: '100vh', 
      display: 'flex', 
      flexDirection: 'column', 
      justifyContent: 'center',
      background: 'var(--color-background)'
    }}>
      <h2 style={{ color: 'var(--color-text)', marginBottom: '1rem' }}>Failed to load portfolio</h2>
      <p style={{ color: 'var(--color-text-muted)', marginBottom: '1rem' }}>{error}</p>
      <p style={{ marginTop: '1rem', fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>
        Make sure the backend is running on <code style={{ 
          background: 'var(--color-surface)', 
          padding: '0.25rem 0.5rem', 
          borderRadius: '4px',
          color: 'var(--color-accent)'
        }}>http://localhost:8000</code>
      </p>
    </div>
  )
  if (!data || !data.profile) return <div style={{
    background: 'var(--color-background)',
    color: 'var(--color-text)',
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }}>No data available</div>

  return (
    <>
      <Navbar />
      <main>
        <Hero profile={data.profile} />
        
        {/* About Section */}
        <section id="about" className="section">
          <div className="container">
            <SectionHeader title="About Me" subtitle="Get to know me better" />
            <div style={{ 
              maxWidth: '800px', 
              margin: '0 auto',
              background: 'var(--color-surface)',
              border: '1px solid var(--color-border)',
              borderRadius: 'var(--radius-xl)',
              padding: 'var(--spacing-8)',
              boxShadow: 'var(--shadow-lg)'
            }}>
              <p style={{ 
                fontSize: 'var(--text-lg)', 
                lineHeight: '1.8',
                color: 'var(--color-text)',
                marginBottom: 'var(--spacing-4)'
              }}>{data.profile.bio}</p>
              <div style={{
                display: 'flex',
                gap: 'var(--spacing-6)',
                flexWrap: 'wrap',
                paddingTop: 'var(--spacing-6)',
                borderTop: '1px solid var(--color-border)'
              }}>
                <div>
                  <div style={{ 
                    color: 'var(--color-text-muted)', 
                    fontSize: 'var(--text-sm)',
                    marginBottom: 'var(--spacing-1)'
                  }}>Location</div>
                  <div style={{ color: 'var(--color-text)', fontWeight: '500' }}>{data.profile.location}</div>
                </div>
                <div>
                  <div style={{ 
                    color: 'var(--color-text-muted)', 
                    fontSize: 'var(--text-sm)',
                    marginBottom: 'var(--spacing-1)'
                  }}>Email</div>
                  <a href={`mailto:${data.profile.email}`} style={{ 
                    color: 'var(--color-secondary)', 
                    fontWeight: '500',
                    textDecoration: 'none'
                  }}>{data.profile.email}</a>
                </div>
                <div>
                  <div style={{ 
                    color: 'var(--color-text-muted)', 
                    fontSize: 'var(--text-sm)',
                    marginBottom: 'var(--spacing-1)'
                  }}>Phone</div>
                  <div style={{ color: 'var(--color-text)', fontWeight: '500' }}>{data.profile.phone}</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Education Section */}
        <section id="education" className="section">
          <div className="container">
            <SectionHeader title="Education" subtitle="My academic journey" />
            <div style={{ display: 'grid', gap: 'var(--spacing-6)', maxWidth: '900px', margin: '0 auto' }}>
              {data.education.map(edu => (
                <div key={edu.id} className="card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 'var(--spacing-3)' }}>
                    <div style={{ flex: 1 }}>
                      <h3 style={{ 
                        fontSize: 'var(--text-2xl)', 
                        marginBottom: 'var(--spacing-2)',
                        color: 'var(--color-text)'
                      }}>{edu.degree}</h3>
                      <div style={{ 
                        fontSize: 'var(--text-lg)', 
                        color: 'var(--color-secondary)',
                        fontWeight: '600',
                        marginBottom: 'var(--spacing-2)'
                      }}>{edu.field_of_study}</div>
                    </div>
                    <Badge label={edu.end_date || 'Present'} variant="accent" />
                  </div>
                  <div style={{ 
                    display: 'flex', 
                    gap: 'var(--spacing-4)', 
                    color: 'var(--color-text-muted)',
                    marginBottom: 'var(--spacing-3)',
                    fontSize: 'var(--text-sm)'
                  }}>
                    <span>🎓 {edu.institution}</span>
                    {edu.location && <span>📍 {edu.location}</span>}
                  </div>
                  {edu.grade && (
                    <div style={{ 
                      background: 'rgba(16, 185, 129, 0.1)', 
                      padding: 'var(--spacing-2) var(--spacing-3)',
                      borderRadius: 'var(--radius-md)',
                      display: 'inline-block',
                      color: 'var(--color-accent)',
                      fontSize: 'var(--text-sm)',
                      fontWeight: '600',
                      marginBottom: 'var(--spacing-3)'
                    }}>
                      Grade: {edu.grade}
                    </div>
                  )}
                  {edu.description && (
                    <p style={{ color: 'var(--color-text-muted)', lineHeight: '1.6' }}>
                      {edu.description}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Experience Section */}
        <section id="experience" className="section">
          <div className="container">
            <SectionHeader title="Experience" subtitle="My professional journey" />
            <div style={{ display: 'grid', gap: 'var(--spacing-6)', maxWidth: '900px', margin: '0 auto' }}>
              {data.experience.map(exp => (
                <div key={exp.id} className="card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 'var(--spacing-3)', flexWrap: 'wrap', gap: 'var(--spacing-3)' }}>
                    <div style={{ flex: 1 }}>
                      <h3 style={{ 
                        fontSize: 'var(--text-2xl)', 
                        marginBottom: 'var(--spacing-2)',
                        color: 'var(--color-text)'
                      }}>{exp.title}</h3>
                      <div style={{ 
                        fontSize: 'var(--text-lg)', 
                        color: 'var(--color-secondary)',
                        fontWeight: '600',
                        marginBottom: 'var(--spacing-2)'
                      }}>{exp.company}</div>
                    </div>
                    <Badge label={exp.is_current ? 'Current' : `${exp.start_date} - ${exp.end_date}`} variant={exp.is_current ? 'accent' : 'default'} />
                  </div>
                  <div style={{ 
                    display: 'flex', 
                    gap: 'var(--spacing-4)', 
                    color: 'var(--color-text-muted)',
                    marginBottom: 'var(--spacing-4)',
                    fontSize: 'var(--text-sm)',
                    flexWrap: 'wrap'
                  }}>
                    {exp.location && <span>📍 {exp.location}</span>}
                    {exp.employment_type && <span>💼 {exp.employment_type}</span>}
                    {!exp.is_current && <span>📅 {exp.start_date} - {exp.end_date}</span>}
                  </div>
                  {exp.description && (
                    <p style={{ 
                      color: 'var(--color-text-muted)', 
                      lineHeight: '1.7',
                      marginBottom: 'var(--spacing-4)'
                    }}>{exp.description}</p>
                  )}
                  {exp.responsibilities && exp.responsibilities.length > 0 && (
                    <div style={{ marginBottom: 'var(--spacing-4)' }}>
                      <div style={{ 
                        color: 'var(--color-text)', 
                        fontWeight: '600',
                        marginBottom: 'var(--spacing-2)',
                        fontSize: 'var(--text-sm)',
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em'
                      }}>Key Responsibilities</div>
                      <ul style={{ 
                        listStyle: 'none', 
                        padding: 0,
                        display: 'grid',
                        gap: 'var(--spacing-2)'
                      }}>
                        {exp.responsibilities.map((resp, idx) => (
                          <li key={idx} style={{ 
                            paddingLeft: 'var(--spacing-4)', 
                            position: 'relative',
                            color: 'var(--color-text-muted)',
                            lineHeight: '1.6'
                          }}>
                            <span style={{ 
                              position: 'absolute', 
                              left: 0, 
                              color: 'var(--color-accent)'
                            }}>▸</span>
                            {resp}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {exp.technologies && exp.technologies.length > 0 && (
                    <div>
                      <div style={{ 
                        color: 'var(--color-text)', 
                        fontWeight: '600',
                        marginBottom: 'var(--spacing-3)',
                        fontSize: 'var(--text-sm)',
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em'
                      }}>Technologies</div>
                      <div style={{ display: 'flex', gap: 'var(--spacing-2)', flexWrap: 'wrap' }}>
                        {exp.technologies.map((tech, idx) => (
                          <span key={idx} className="tag">{tech}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Skills Section */}
        <section id="skills" className="section">
          <div className="container">
            <SectionHeader title="Skills & Technologies" subtitle="My technical toolkit" />
            <div style={{ 
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
              gap: 'var(--spacing-6)',
              maxWidth: '1100px',
              margin: '0 auto'
            }}>
              {Object.entries(data.skills).map(([category, skills]) => (
                <div key={category} className="card">
                  <h3 style={{ 
                    fontSize: 'var(--text-xl)', 
                    marginBottom: 'var(--spacing-4)',
                    background: 'var(--gradient-primary)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text',
                    fontWeight: '700'
                  }}>{category}</h3>
                  <div style={{ display: 'flex', gap: 'var(--spacing-2)', flexWrap: 'wrap' }}>
                    {skills.map((skill) => (
                      <span key={skill.id} className="tag" style={{
                        cursor: 'pointer',
                        transition: 'all 0.2s'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.background = 'rgba(99, 102, 241, 0.25)'
                        e.currentTarget.style.transform = 'translateY(-2px)'
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.background = 'rgba(99, 102, 241, 0.12)'
                        e.currentTarget.style.transform = 'translateY(0)'
                      }}>
                        {skill.name}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Projects Section */}
        <section id="projects" className="section">
          <div className="container">
            <SectionHeader title="Projects" subtitle="Things I've built" />
            <div style={{ 
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
              gap: 'var(--spacing-6)'
            }}>
              {data.projects.map(project => (
                <div key={project.id} className="card" style={{
                  display: 'flex',
                  flexDirection: 'column',
                  position: 'relative'
                }}>
                  {project.is_featured && (
                    <div style={{
                      position: 'absolute',
                      top: 'var(--spacing-4)',
                      right: 'var(--spacing-4)',
                      background: 'var(--gradient-accent)',
                      color: 'white',
                      padding: '0.25rem 0.75rem',
                      borderRadius: 'var(--radius-full)',
                      fontSize: 'var(--text-xs)',
                      fontWeight: '600',
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em',
                      boxShadow: 'var(--shadow-glow-accent)'
                    }}>Featured</div>
                  )}
                  <h3 style={{ 
                    fontSize: 'var(--text-xl)', 
                    marginBottom: 'var(--spacing-2)',
                    color: 'var(--color-text)',
                    fontWeight: '700'
                  }}>{project.name}</h3>
                  <p style={{ 
                    color: 'var(--color-text-muted)',
                    marginBottom: 'var(--spacing-4)',
                    lineHeight: '1.6',
                    flex: 1
                  }}>{project.short_description}</p>
                  {project.technologies && project.technologies.length > 0 && (
                    <div style={{ 
                      display: 'flex', 
                      gap: 'var(--spacing-2)', 
                      flexWrap: 'wrap',
                      marginBottom: 'var(--spacing-4)'
                    }}>
                      {project.technologies.slice(0, 4).map((tech, idx) => (
                        <span key={idx} className="tag">{tech}</span>
                      ))}
                      {project.technologies.length > 4 && (
                        <span className="tag" style={{ background: 'rgba(148, 163, 184, 0.1)', border: '1px solid rgba(148, 163, 184, 0.25)' }}>
                          +{project.technologies.length - 4} more
                        </span>
                      )}
                    </div>
                  )}
                  <div style={{ 
                    display: 'flex', 
                    gap: 'var(--spacing-3)',
                    paddingTop: 'var(--spacing-4)',
                    borderTop: '1px solid var(--color-border)'
                  }}>
                    {project.github_url && (
                      <a href={project.github_url} target="_blank" rel="noopener noreferrer" style={{
                        color: 'var(--color-secondary)',
                        fontSize: 'var(--text-sm)',
                        fontWeight: '600',
                        textDecoration: 'none',
                        display: 'flex',
                        alignItems: 'center',
                        gap: 'var(--spacing-1)',
                        transition: 'all 0.2s'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.color = 'var(--color-accent)'
                        e.currentTarget.style.transform = 'translateX(3px)'
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.color = 'var(--color-secondary)'
                        e.currentTarget.style.transform = 'translateX(0)'
                      }}>
                        View Code →
                      </a>
                    )}
                    <span style={{
                      marginLeft: 'auto',
                      fontSize: 'var(--text-xs)',
                      padding: '0.25rem 0.5rem',
                      borderRadius: 'var(--radius-md)',
                      background: project.status === 'completed' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(251, 191, 36, 0.1)',
                      color: project.status === 'completed' ? 'var(--color-accent)' : '#FCD34D',
                      fontWeight: '600',
                      textTransform: 'capitalize'
                    }}>{project.status}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Achievements Section */}
        <section id="achievements" className="section">
          <div className="container">
            <SectionHeader title="Achievements" subtitle="Milestones and recognitions" />
            <div style={{ 
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
              gap: 'var(--spacing-6)',
              maxWidth: '1100px',
              margin: '0 auto'
            }}>
              {data.achievements.map(ach => (
                <div key={ach.id} className="card" style={{
                  textAlign: 'center',
                  padding: 'var(--spacing-8)'
                }}>
                  <div style={{
                    fontSize: '3rem',
                    marginBottom: 'var(--spacing-3)',
                    filter: 'drop-shadow(0 0 10px rgba(16, 185, 129, 0.5))'
                  }}>
                    {ach.icon === 'award' && '🏆'}
                    {ach.icon === 'star' && '⭐'}
                    {ach.icon === 'graduation' && '🎓'}
                    {ach.icon === 'trophy' && '🥇'}
                  </div>
                  <h4 style={{
                    fontSize: 'var(--text-lg)',
                    marginBottom: 'var(--spacing-2)',
                    color: 'var(--color-text)',
                    fontWeight: '600'
                  }}>{ach.title}</h4>
                  <div style={{
                    color: 'var(--color-secondary)',
                    fontWeight: '600',
                    marginBottom: 'var(--spacing-2)',
                    fontSize: 'var(--text-sm)'
                  }}>{ach.issuer}</div>
                  <Badge label={ach.date} variant="accent" />
                  {ach.description && (
                    <p style={{
                      color: 'var(--color-text-muted)',
                      marginTop: 'var(--spacing-3)',
                      fontSize: 'var(--text-sm)',
                      lineHeight: '1.6'
                    }}>{ach.description}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Resume Section */}
        <section id="resume" className="section">
          <div className="container" style={{ textAlign: 'center' }}>
            <SectionHeader title="Resume" subtitle="Download my complete resume" />
            <div style={{
              maxWidth: '600px',
              margin: '0 auto',
              background: 'var(--color-surface)',
              border: '1px solid var(--color-border)',
              borderRadius: 'var(--radius-xl)',
              padding: 'var(--spacing-10)',
              boxShadow: 'var(--shadow-lg)'
            }}>
              <div style={{
                fontSize: '4rem',
                marginBottom: 'var(--spacing-4)',
                filter: 'drop-shadow(0 0 10px rgba(99, 102, 241, 0.5))'
              }}>📄</div>
              <h3 style={{
                fontSize: 'var(--text-2xl)',
                marginBottom: 'var(--spacing-3)',
                color: 'var(--color-text)'
              }}>Get My Full Resume</h3>
              <p style={{
                color: 'var(--color-text-muted)',
                marginBottom: 'var(--spacing-6)',
                lineHeight: '1.6'
              }}>
                Download my complete resume with detailed information about my experience, education, and skills.
              </p>
              <a href="http://localhost:8000/api/v1/resume/download" download style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 'var(--spacing-2)',
                padding: 'var(--spacing-4) var(--spacing-8)',
                background: 'var(--gradient-primary)',
                color: 'white',
                borderRadius: 'var(--radius-lg)',
                textDecoration: 'none',
                fontWeight: '600',
                fontSize: 'var(--text-base)',
                boxShadow: 'var(--shadow-glow)',
                transition: 'all 0.3s',
                position: 'relative',
                overflow: 'hidden'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-3px)'
                e.currentTarget.style.boxShadow = '0 0 30px rgba(99, 102, 241, 0.6)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)'
                e.currentTarget.style.boxShadow = 'var(--shadow-glow)'
              }}>
                Download Resume
                <span style={{ fontSize: '1.25rem' }}>⬇</span>
              </a>
            </div>
          </div>
        </section>

        <section id="contact" className="section">
          <div className="container">
            <h2>Contact</h2>
            <p>Email: {data.profile.email}</p>
            <p>Location: {data.profile.location}</p>
          </div>
        </section>
      </main>

      <footer style={{
        background: 'var(--color-primary)',
        color: 'white',
        padding: '2rem',
        textAlign: 'center'
      }}>
        <p>© 2024 {data.profile.full_name}. All rights reserved.</p>
      </footer>
    </>
  )
}

export default App
