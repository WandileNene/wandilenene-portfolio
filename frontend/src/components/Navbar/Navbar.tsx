import { useState, useEffect } from 'react'
import styles from './Navbar.module.css'

const NAV_LINKS = [
  { href: '#about', label: 'About' },
  { href: '#education', label: 'Education' },
  { href: '#experience', label: 'Experience' },
  { href: '#skills', label: 'Skills' },
  { href: '#projects', label: 'Projects' },
  { href: '#achievements', label: 'Achievements' },
  { href: '#resume', label: 'Resume' },
  { href: '#contact', label: 'Contact' },
]

export function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isScrolled, setIsScrolled] = useState(false)
  const [activeSection, setActiveSection] = useState('')

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)

      // Highlight active section
      const sections = NAV_LINKS.map(link => link.href.slice(1))
      for (let i = sections.length - 1; i >= 0; i--) {
        const el = document.getElementById(sections[i])
        if (el && window.scrollY >= el.offsetTop - 120) {
          setActiveSection(sections[i])
          break
        }
      }
    }

    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const handleLinkClick = (href: string) => {
    setIsMenuOpen(false)
    const id = href.slice(1)
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <header className={`${styles.header} ${isScrolled ? styles.scrolled : ''}`} role="banner">
      <nav className={`${styles.nav} container`} aria-label="Main navigation">
        <a href="#" className={styles.logo} onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
          <span className={styles.logoText}>WN</span>
          <span className={styles.logoDot} aria-hidden="true" />
        </a>

        {/* Desktop Navigation */}
        <ul className={styles.links} role="list">
          {NAV_LINKS.map(link => (
            <li key={link.href}>
              <a
                href={link.href}
                className={`${styles.link} ${activeSection === link.href.slice(1) ? styles.active : ''}`}
                onClick={e => { e.preventDefault(); handleLinkClick(link.href) }}
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        {/* Mobile Menu Button */}
        <button
          className={styles.menuBtn}
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          aria-expanded={isMenuOpen}
          aria-label={isMenuOpen ? 'Close menu' : 'Open menu'}
        >
          <span className={`${styles.menuBar} ${isMenuOpen ? styles.menuBarOpen1 : ''}`} />
          <span className={`${styles.menuBar} ${isMenuOpen ? styles.menuBarOpen2 : ''}`} />
          <span className={`${styles.menuBar} ${isMenuOpen ? styles.menuBarOpen3 : ''}`} />
        </button>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className={styles.mobileMenu} role="dialog" aria-label="Mobile navigation">
            <ul role="list">
              {NAV_LINKS.map(link => (
                <li key={link.href}>
                  <a
                    href={link.href}
                    className={`${styles.mobileLink} ${activeSection === link.href.slice(1) ? styles.active : ''}`}
                    onClick={e => { e.preventDefault(); handleLinkClick(link.href) }}
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </nav>
    </header>
  )
}
