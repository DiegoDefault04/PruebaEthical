import Image from "next/image";
import Link from "next/link";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <Image
          className={styles.logo}
          src="/next.svg"
          alt="Next.js logo"
          width={100}
          height={20}
          priority
        />

        <div className={styles.intro}>
          <h1>Diego Alberto Martinez Hernandez</h1>
          <p>
            Prueba Tecnica
            Endpoints para probar desde Postman
          </p>
        </div>

        {/* ✅ UN SOLO CTAS */}
        <div className={styles.ctas}>
          <Link href="https://github.com/DiegoDefault04" className={styles.primary}>
            <Image
              className={styles.logo}
              src="/vercel.svg"
              alt="Login"
              width={16}
              height={16}
            />
            GitHub
          </Link>

          <Link href="/login" className={styles.primary}>
            <Image
              className={styles.logo}
              src="/vercel.svg"
              alt="Login"
              width={16}
              height={16}
            />
            Login
          </Link>
        </div>
      </main>
    </div>
  );
}
