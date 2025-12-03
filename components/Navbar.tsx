"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Search, Upload, Heart } from "lucide-react"
import { motion } from "framer-motion"

export default function Navbar() {
  const pathname = usePathname()

  const navItems = [
    { href: "/", label: "Home", icon: Search },
    { href: "/upload", label: "Upload", icon: Upload },
    { href: "/consultation", label: "Consultation", icon: Heart },
  ]

  return (
    <nav className="sticky top-0 z-50 w-full border-b-2 border-gray-300 dark:border-gray-700 bg-white/95 dark:bg-gray-900/95 backdrop-blur-md shadow-lg">
      <div className="container mx-auto px-6">
        <div className="flex h-20 items-center justify-between">
          <Link href="/" className="flex items-center space-x-3 group">
            <motion.div
              whileHover={{ scale: 1.1, rotate: 5 }}
              whileTap={{ scale: 0.95 }}
              className="transition-transform"
            >
              <div className="p-2.5 gradient-primary shadow-lg shadow-primary/30">
                <Search className="h-6 w-6 text-white" />
              </div>
            </motion.div>
            <span className="text-2xl font-black tracking-tight text-gray-900 dark:text-white uppercase group-hover:text-primary transition-colors">
              FindMe
            </span>
          </Link>

          <div className="flex items-center space-x-3">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = pathname === item.href
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`relative flex items-center space-x-2 px-6 py-3 text-sm font-bold uppercase tracking-wider transition-all duration-300 border-2 ${
                    isActive
                      ? "gradient-primary text-white border-primary shadow-lg shadow-primary/30 scale-105"
                      : "bg-transparent text-gray-700 dark:text-gray-300 border-transparent hover:bg-gray-100 dark:hover:bg-gray-800 hover:border-gray-300 dark:hover:border-gray-600 hover:scale-105"
                  }`}
                >
                  <Icon className={`h-4 w-4 ${isActive ? "animate-pulse" : ""}`} />
                  <span>{item.label}</span>
                  {isActive && (
                    <motion.div
                      layoutId="activeTab"
                      className="absolute inset-0 border-2 border-primary bg-primary/10"
                      transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                    />
                  )}
                </Link>
              )
            })}
          </div>
        </div>
      </div>
    </nav>
  )
}

