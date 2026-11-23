import { useState } from 'react'
import { portfolioAPI } from '../../services/api'
import styles from './ContactForm.module.css'

type FormState = 'idle' | 'submitting' | 'success' | 'error'

interface FormFields {
  name: string
  email: string
  subject: string
  message: string
}

const EMPTY: FormFields = { name: '', email: '', subject: '', message: '' }

function validate(fields: FormFields): Partial<FormFields> {
  const errors: Partial<FormFields> = {}
  if (!fields.name.trim()) errors.name = 'Name is required'
  if (!fields.email.trim()) {
    errors.email = 'Email is required'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(fields.email)) {
    errors.email = 'Enter a valid email address'
  }
  if (!fields.message.trim()) errors.message = 'Message is required'
  else if (fields.message.trim().length < 10) errors.message = 'Message must be at least 10 characters'
  return errors
}

export function ContactForm() {
  const [fields, setFields] = useState<FormFields>(EMPTY)
  const [touched, setTouched] = useState<Partial<Record<keyof FormFields, boolean>>>({})
  const [formState, setFormState] = useState<FormState>('idle')
  const [errorMsg, setErrorMsg] = useState('')

  const errors = validate(fields)
  const isValid = Object.keys(errors).length === 0

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFields(prev => ({ ...prev, [name]: value }))
  }

  const handleBlur = (e: React.FocusEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setTouched(prev => ({ ...prev, [e.target.name]: true }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // Mark all fields touched to show all errors on submit attempt
    setTouched({ name: true, email: true, subject: true, message: true })
    if (!isValid) return

    setFormState('submitting')
    setErrorMsg('')
    try {
      await portfolioAPI.sendContactMessage({
        name: fields.name.trim(),
        email: fields.email.trim(),
        subject: fields.subject.trim() || undefined,
        message: fields.message.trim(),
      })
      setFormState('success')
      setFields(EMPTY)
      setTouched({})
    } catch (err) {
      setFormState('error')
      setErrorMsg(err instanceof Error ? err.message : 'Something went wrong. Please try again.')
    }
  }

  if (formState === 'success') {
    return (
      <div className={styles.successBox} role="alert">
        <div className={styles.successIcon} aria-hidden="true">✅</div>
        <h3 className={styles.successTitle}>Message Sent!</h3>
        <p className={styles.successText}>
          Thanks for reaching out. I'll get back to you as soon as possible.
        </p>
        <button className={styles.resetBtn} onClick={() => setFormState('idle')}>
          Send Another Message
        </button>
      </div>
    )
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit} noValidate aria-label="Contact form">
      <div className={styles.row}>
        {/* Name */}
        <div className={styles.field}>
          <label className={styles.label} htmlFor="contact-name">
            Full Name <span className={styles.required} aria-hidden="true">*</span>
          </label>
          <input
            id="contact-name"
            name="name"
            type="text"
            autoComplete="name"
            placeholder="Your name"
            value={fields.name}
            onChange={handleChange}
            onBlur={handleBlur}
            aria-required="true"
            aria-invalid={touched.name && !!errors.name}
            aria-describedby={touched.name && errors.name ? 'err-name' : undefined}
            className={`${styles.input} ${touched.name && errors.name ? styles.inputError : ''}`}
          />
          {touched.name && errors.name && (
            <span id="err-name" className={styles.errorText} role="alert">{errors.name}</span>
          )}
        </div>

        {/* Email */}
        <div className={styles.field}>
          <label className={styles.label} htmlFor="contact-email">
            Email Address <span className={styles.required} aria-hidden="true">*</span>
          </label>
          <input
            id="contact-email"
            name="email"
            type="email"
            autoComplete="email"
            placeholder="you@example.com"
            value={fields.email}
            onChange={handleChange}
            onBlur={handleBlur}
            aria-required="true"
            aria-invalid={touched.email && !!errors.email}
            aria-describedby={touched.email && errors.email ? 'err-email' : undefined}
            className={`${styles.input} ${touched.email && errors.email ? styles.inputError : ''}`}
          />
          {touched.email && errors.email && (
            <span id="err-email" className={styles.errorText} role="alert">{errors.email}</span>
          )}
        </div>
      </div>

      {/* Subject */}
      <div className={styles.field}>
        <label className={styles.label} htmlFor="contact-subject">
          Subject <span className={styles.optional}>(optional)</span>
        </label>
        <input
          id="contact-subject"
          name="subject"
          type="text"
          placeholder="What's this about?"
          value={fields.subject}
          onChange={handleChange}
          onBlur={handleBlur}
          className={styles.input}
        />
      </div>

      {/* Message */}
      <div className={styles.field}>
        <label className={styles.label} htmlFor="contact-message">
          Message <span className={styles.required} aria-hidden="true">*</span>
        </label>
        <textarea
          id="contact-message"
          name="message"
          rows={6}
          placeholder="Tell me what you have in mind..."
          value={fields.message}
          onChange={handleChange}
          onBlur={handleBlur}
          aria-required="true"
          aria-invalid={touched.message && !!errors.message}
          aria-describedby={touched.message && errors.message ? 'err-message' : undefined}
          className={`${styles.textarea} ${touched.message && errors.message ? styles.inputError : ''}`}
        />
        <div className={styles.charCount}>{fields.message.length} characters</div>
        {touched.message && errors.message && (
          <span id="err-message" className={styles.errorText} role="alert">{errors.message}</span>
        )}
      </div>

      {/* API error banner */}
      {formState === 'error' && (
        <div className={styles.errorBanner} role="alert">
          <span aria-hidden="true">⚠️</span> {errorMsg}
        </div>
      )}

      <button
        type="submit"
        className={styles.submitBtn}
        disabled={formState === 'submitting'}
        aria-busy={formState === 'submitting'}
      >
        {formState === 'submitting' ? (
          <>
            <span className={styles.spinner} aria-hidden="true" />
            Sending…
          </>
        ) : (
          <>
            Send Message
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
          </>
        )}
      </button>
    </form>
  )
}
