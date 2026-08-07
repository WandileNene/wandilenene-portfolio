import styles from './LoadingSpinner.module.css'

export function LoadingSpinner() {
  return (
    <div className={styles.container} role="status" aria-label="Loading portfolio data">
      <div className={styles.spinner} />
      <p className={styles.text}>Loading portfolio...</p>
    </div>
  )
}
