"use client"

import Link from "next/link"
import { motion } from "framer-motion"
import { Upload, Search, Phone, ArrowRight, Heart, Shield, Users, AlertCircle, UsersRound, Scale, MessageCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function HomePage() {
  return (
    <div className="flex flex-col bg-[#FAFAFA] dark:bg-gray-900">
      {/* Hero Section */}
      <section className="relative min-h-[100vh] flex items-center justify-center overflow-hidden border-b-2 border-gray-300 dark:border-gray-700">
        {/* Background Image with Overlay */}
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='1920' height='1080' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='grad' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%231e3a8a;stop-opacity:0.9'/%3E%3Cstop offset='50%25' style='stop-color:%231e40af;stop-opacity:0.8'/%3E%3Cstop offset='100%25' style='stop-color:%231e293b;stop-opacity:0.9'/%3E%3C/linearGradient%3E%3Cpattern id='grid' width='40' height='40' patternUnits='userSpaceOnUse'%3E%3Cpath d='M 40 0 L 0 0 0 40' fill='none' stroke='rgba(255,255,255,0.05)' stroke-width='1'/%3E%3C/pattern%3E%3C/defs%3E%3Crect width='100%25' height='100%25' fill='url(%23grad)'/%3E%3Crect width='100%25' height='100%25' fill='url(%23grid)'/%3E%3Cpath d='M0,400 Q480,300 960,400 T1920,400' fill='none' stroke='rgba(255,255,255,0.1)' stroke-width='2'/%3E%3Cpath d='M0,600 Q480,500 960,600 T1920,600' fill='none' stroke='rgba(255,255,255,0.1)' stroke-width='2'/%3E%3C/svg%3E")`,
          }}
        />
        {/* Dark Overlay for better text readability */}
        <div className="absolute inset-0 bg-gradient-to-br from-gray-900/85 via-gray-800/75 to-gray-900/85 dark:from-gray-900/90 dark:via-gray-800/80 dark:to-gray-900/90" />
        
        {/* Animated grid pattern overlay */}
        <motion.div
          animate={{
            opacity: [0.1, 0.2, 0.1],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="absolute inset-0"
          style={{
            backgroundImage: `repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px),
                             repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px)`,
            backgroundSize: "40px 40px",
          }}
        />
        
        {/* Animated background elements */}
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.3, 0.5, 0.3],
              x: [0, 100, 0],
              y: [0, 50, 0],
            }}
            transition={{
              duration: 8,
              repeat: Infinity,
              ease: "easeInOut",
            }}
            className="absolute top-20 left-10 w-72 h-72 bg-primary/20 rounded-full blur-3xl"
          />
          <motion.div
            animate={{
              scale: [1, 1.3, 1],
              opacity: [0.2, 0.4, 0.2],
              x: [0, -80, 0],
              y: [0, -60, 0],
            }}
            transition={{
              duration: 10,
              repeat: Infinity,
              ease: "easeInOut",
              delay: 1,
            }}
            className="absolute bottom-20 right-10 w-96 h-96 bg-red-500/20 rounded-full blur-3xl"
          />
          <motion.div
            animate={{
              scale: [1, 1.1, 1],
              opacity: [0.1, 0.3, 0.1],
              rotate: [0, 180, 360],
            }}
            transition={{
              duration: 15,
              repeat: Infinity,
              ease: "linear",
            }}
            className="absolute top-1/2 left-1/2 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2"
          />
        </div>
        
        <div className="relative z-10 container mx-auto px-6 py-20 text-center">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8 }}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.8, y: -20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.6, type: "spring", stiffness: 200 }}
              whileHover={{ scale: 1.05 }}
              className="inline-block mb-8 px-5 py-2.5 bg-gradient-to-r from-red-500 to-red-600 text-white font-bold text-sm uppercase tracking-wider shadow-lg shadow-red-500/50 backdrop-blur-sm"
            >
              <AlertCircle className="inline h-4 w-4 mr-2" />
              ⚠️ Hackathon Submission - ARM AI Challenge
            </motion.div>
            
            {/* 4 Help Divs Around FindMe */}
            <div className="relative mb-8 flex flex-col items-center w-full">
              {/* Top Divs */}
              <div className="flex flex-wrap justify-center gap-5 md:gap-6 lg:gap-8 mb-8 md:mb-12 w-full max-w-7xl mx-auto px-4">
                {[
                  {
                    title: "Helping Solve Human Trafficking",
                    description: "Advanced detection and rescue operations",
                    icon: Shield,
                    delay: 0.3,
                    color: "from-red-600 to-red-700",
                    hoverColor: "hover:shadow-red-500/40",
                  },
                  {
                    title: "Find Missing People",
                    description: "AI-powered search and matching system",
                    icon: Search,
                    delay: 0.4,
                    color: "from-primary to-blue-700",
                    hoverColor: "hover:shadow-primary/40",
                  },
                ].map((item, index) => {
                  const Icon = item.icon
                  return (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, scale: 0.5, y: -50, rotate: -10 }}
                      animate={{ opacity: 1, scale: 1, y: 0, rotate: 0 }}
                      transition={{ 
                        delay: item.delay, 
                        duration: 0.8,
                        type: "spring",
                        stiffness: 100,
                        damping: 10
                      }}
                      whileHover={{ 
                        scale: 1.05, 
                        y: -8,
                        rotate: 1,
                        transition: { duration: 0.3 }
                      }}
                      whileTap={{ scale: 0.98 }}
                      className="bg-gradient-to-br from-white/10 via-white/5 to-transparent backdrop-blur-2xl border border-white/20 p-6 md:p-8 lg:p-10 shadow-lg hover:shadow-xl hover:border-white/30 transition-all duration-500 group flex-1 min-w-[280px] md:min-w-[300px] lg:min-w-[320px] max-w-[380px] lg:max-w-[400px] rounded-[3rem] md:rounded-[4rem] relative overflow-hidden"
                    >
                      {/* Subtle gradient overlay */}
                      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-red-500/5 opacity-50 pointer-events-none" />
                      
                      <motion.div
                        animate={{ 
                          rotate: [0, 3, -3, 0],
                        }}
                        transition={{
                          duration: 4,
                          repeat: Infinity,
                          repeatDelay: 2,
                        }}
                        className="flex flex-col items-center text-center h-full relative z-10"
                      >
                        <motion.div
                          whileHover={{ rotate: 360, scale: 1.1 }}
                          transition={{ duration: 0.6 }}
                          className={`p-4 md:p-5 bg-gradient-to-br ${item.color} mb-4 md:mb-5 shadow-2xl ${item.hoverColor} transition-all duration-300 rounded-full`}
                        >
                          <Icon className="h-7 w-7 md:h-9 md:w-9 text-white" />
                        </motion.div>
                        <motion.h3
                          whileHover={{ scale: 1.03 }}
                          className="text-base md:text-lg lg:text-xl font-black uppercase tracking-tight text-white mb-3 md:mb-4 group-hover:text-blue-200 transition-colors leading-tight px-4"
                          style={{
                            textShadow: "0 2px 10px rgba(0,0,0,0.5), 0 4px 20px rgba(0,0,0,0.3)",
                          }}
                        >
                          {item.title}
                        </motion.h3>
                        <p 
                          className="text-sm md:text-base lg:text-lg text-gray-200 font-semibold leading-relaxed px-4"
                          style={{
                            textShadow: "0 2px 8px rgba(0,0,0,0.4), 0 1px 3px rgba(0,0,0,0.3)",
                          }}
                        >
                          {item.description}
                        </p>
                      </motion.div>
                    </motion.div>
                  )
                })}
              </div>
              
              {/* Center FindMe Title with enhanced animation */}
              <motion.div
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ 
                  delay: 0.6, 
                  duration: 1,
                  type: "spring",
                  stiffness: 100
                }}
                whileHover={{ scale: 1.05 }}
                className="mb-6 md:mb-10 lg:mb-12 w-full"
              >
                <motion.h1
                  animate={{
                    backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"],
                  }}
                  transition={{
                    duration: 5,
                    repeat: Infinity,
                    ease: "linear",
                  }}
                  className="text-6xl md:text-8xl lg:text-9xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white via-blue-200 to-white bg-[length:200%_auto] uppercase tracking-tight leading-tight"
                  style={{
                    WebkitBackgroundClip: "text",
                    WebkitTextFillColor: "transparent",
                  }}
                >
                  FindMe
                </motion.h1>
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: "100%" }}
                  transition={{ delay: 1, duration: 1, ease: "easeOut" }}
                  className="h-1 bg-gradient-to-r from-transparent via-white to-transparent mx-auto mt-4"
                />
              </motion.div>
              
              {/* Bottom Divs */}
              <div className="flex flex-wrap justify-center gap-5 md:gap-6 lg:gap-8 w-full max-w-7xl mx-auto px-4">
                {[
                  {
                    title: "Detect Criminals",
                    description: "Advanced facial recognition and database matching",
                    icon: UsersRound,
                    delay: 0.7,
                    color: "from-gray-800 to-gray-900",
                    hoverColor: "hover:shadow-gray-500/40",
                  },
                  {
                    title: "Consultation",
                    description: "24/7 professional support and guidance",
                    icon: MessageCircle,
                    delay: 0.8,
                    color: "from-blue-600 to-primary",
                    hoverColor: "hover:shadow-blue-500/40",
                  },
                ].map((item, index) => {
                  const Icon = item.icon
                  return (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, scale: 0.5, y: 50, rotate: 10 }}
                      animate={{ opacity: 1, scale: 1, y: 0, rotate: 0 }}
                      transition={{ 
                        delay: item.delay, 
                        duration: 0.8,
                        type: "spring",
                        stiffness: 100,
                        damping: 10
                      }}
                      whileHover={{ 
                        scale: 1.05, 
                        y: -8,
                        rotate: -1,
                        transition: { duration: 0.3 }
                      }}
                      whileTap={{ scale: 0.98 }}
                      className="bg-gradient-to-br from-white/10 via-white/5 to-transparent backdrop-blur-2xl border border-white/20 p-6 md:p-8 lg:p-10 shadow-lg hover:shadow-xl hover:border-white/30 transition-all duration-500 group flex-1 min-w-[280px] md:min-w-[300px] lg:min-w-[320px] max-w-[380px] lg:max-w-[400px] rounded-[3rem] md:rounded-[4rem] relative overflow-hidden"
                    >
                      {/* Subtle gradient overlay */}
                      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-red-500/5 opacity-50 pointer-events-none" />
                      
                      <motion.div
                        animate={{ 
                          rotate: [0, -3, 3, 0],
                        }}
                        transition={{
                          duration: 4,
                          repeat: Infinity,
                          repeatDelay: 2,
                        }}
                        className="flex flex-col items-center text-center h-full relative z-10"
                      >
                        <motion.div
                          whileHover={{ rotate: -360, scale: 1.1 }}
                          transition={{ duration: 0.6 }}
                          className={`p-4 md:p-5 bg-gradient-to-br ${item.color} mb-4 md:mb-5 shadow-2xl ${item.hoverColor} transition-all duration-300 rounded-full`}
                        >
                          <Icon className="h-7 w-7 md:h-9 md:w-9 text-white" />
                        </motion.div>
                        <motion.h3
                          whileHover={{ scale: 1.03 }}
                          className="text-base md:text-lg lg:text-xl font-black uppercase tracking-tight text-white mb-3 md:mb-4 group-hover:text-blue-200 transition-colors leading-tight px-4"
                          style={{
                            textShadow: "0 2px 10px rgba(0,0,0,0.5), 0 4px 20px rgba(0,0,0,0.3)",
                          }}
                        >
                          {item.title}
                        </motion.h3>
                        <p 
                          className="text-sm md:text-base lg:text-lg text-gray-200 font-semibold leading-relaxed px-4"
                          style={{
                            textShadow: "0 2px 8px rgba(0,0,0,0.4), 0 1px 3px rgba(0,0,0,0.3)",
                          }}
                        >
                          {item.description}
                        </p>
                      </motion.div>
                    </motion.div>
                  )
                })}
              </div>
            </div>
            
            {/* Description and CTA */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1, duration: 0.8, type: "spring", stiffness: 100 }}
              className="mt-12 md:mt-16"
            >
              <motion.p
                animate={{
                  textShadow: [
                    "0 0 20px rgba(255,255,255,0.3)",
                    "0 0 30px rgba(255,255,255,0.5)",
                    "0 0 20px rgba(255,255,255,0.3)",
                  ],
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
                className="text-2xl md:text-3xl lg:text-4xl font-bold text-white mb-6 max-w-4xl mx-auto drop-shadow-2xl"
              >
                Advanced AI-Powered Platform for Missing Persons & Human Trafficking Detection
              </motion.p>
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1.2, duration: 0.8 }}
                className="text-lg md:text-xl text-gray-200 mb-10 max-w-3xl mx-auto font-semibold leading-relaxed"
              >
                Connecting families with missing persons through secure, authoritative reporting and cutting-edge AI technology
              </motion.p>
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 1.4, duration: 0.6, type: "spring", stiffness: 200 }}
                whileHover={{ scale: 1.08, y: -5 }}
                whileTap={{ scale: 0.95 }}
              >
                <Link href="/upload">
                  <motion.div
                    animate={{
                      boxShadow: [
                        "0 10px 40px rgba(30, 58, 138, 0.4)",
                        "0 15px 50px rgba(30, 58, 138, 0.6)",
                        "0 10px 40px rgba(30, 58, 138, 0.4)",
                      ],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                  >
                    <Button size="lg" className="text-base md:text-lg px-8 py-6 gradient-primary shadow-2xl text-white border-2 border-white/20 backdrop-blur-sm">
                      <motion.span
                        animate={{ x: [0, 5, 0] }}
                        transition={{
                          duration: 1.5,
                          repeat: Infinity,
                          ease: "easeInOut",
                        }}
                      >
                        Report Missing Person
                      </motion.span>
                      <motion.div
                        animate={{ x: [0, 5, 0] }}
                        transition={{
                          duration: 1.5,
                          repeat: Infinity,
                          ease: "easeInOut",
                        }}
                      >
                        <ArrowRight className="ml-3 h-5 w-5" />
                      </motion.div>
                    </Button>
                  </motion.div>
                </Link>
              </motion.div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-24 bg-gradient-to-b from-white to-gray-50/50 dark:from-gray-900 dark:to-gray-800/50 border-b-2 border-gray-300 dark:border-gray-700">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-20"
          >
            <h2 className="text-5xl md:text-6xl font-black text-gray-900 dark:text-white mb-6 uppercase tracking-tight">
              How It Works
            </h2>
            <div className="w-24 h-1 bg-gradient-to-r from-primary to-primary/60 mx-auto mb-6 shadow-lg"></div>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto font-semibold">
              Three-step authoritative process for immediate action
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {[
              {
                step: "01",
                title: "Upload Information",
                description: "Submit verified details and high-resolution photos through our secure, encrypted form system.",
                icon: Upload,
                delay: 0.1,
                color: "bg-primary",
              },
              {
                step: "02",
                title: "AI Matching",
                description: "Advanced neural network algorithms cross-reference your submission with national databases and recent sightings.",
                icon: Search,
                delay: 0.2,
                color: "bg-gray-800 dark:bg-gray-700",
              },
              {
                step: "03",
                title: "Contact Authorities",
                description: "Automated integration with law enforcement networks ensures immediate official response and coordination.",
                icon: Phone,
                delay: 0.3,
                color: "bg-red-500",
              },
            ].map((item, index) => {
              const Icon = item.icon
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: item.delay }}
                >
                  <Card className="h-full hover:shadow-2xl hover:shadow-primary/20 transition-all duration-300 border-2 hover:border-primary group bg-white dark:bg-gray-800">
                    <CardHeader className="pb-4">
                      <motion.div
                        whileHover={{ scale: 1.1, rotate: 5 }}
                        className={`w-20 h-20 ${item.color} flex items-center justify-center mb-6 shadow-lg group-hover:shadow-xl transition-shadow`}
                      >
                        <Icon className="h-10 w-10 text-white" />
                      </motion.div>
                      <div className="text-xs font-black text-primary mb-3 uppercase tracking-widest">Step {item.step}</div>
                      <CardTitle className="text-2xl font-black uppercase tracking-tight group-hover:text-primary transition-colors">{item.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <CardDescription className="text-base font-medium leading-relaxed">
                        {item.description}
                      </CardDescription>
                    </CardContent>
                  </Card>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Why This Matters Section */}
      <section className="py-24 bg-[#FAFAFA] dark:bg-gray-800 border-b-2 border-gray-300 dark:border-gray-700">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-20"
          >
            <h2 className="text-5xl md:text-6xl font-black text-gray-900 dark:text-white mb-6 uppercase tracking-tight">
              Why This Matters
            </h2>
            <div className="w-24 h-1 bg-gradient-to-r from-red-500 to-red-600 mx-auto mb-6 shadow-lg"></div>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto font-semibold">
              Every second counts in missing person cases
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {[
              {
                title: "Time is Critical",
                description: "The first 48 hours determine case outcomes. Our platform enables instant submission and real-time database matching for immediate action.",
                icon: Shield,
                stat: "48 HOURS",
                statLabel: "Critical Window",
              },
              {
                title: "Community Network",
                description: "Leverage nationwide visibility through integrated alert systems, social media amplification, and community watch coordination.",
                icon: Users,
                stat: "100%",
                statLabel: "Coverage",
              },
              {
                title: "Professional Support",
                description: "24/7 access to certified crisis counselors, legal assistance, and law enforcement coordination throughout the process.",
                icon: Heart,
                stat: "24/7",
                statLabel: "Support",
              },
            ].map((item, index) => {
              const Icon = item.icon
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.95 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <Card className="h-full hover:shadow-2xl hover:shadow-primary/20 transition-all duration-300 border-2 border-gray-300 dark:border-gray-700 group bg-white dark:bg-gray-800">
                    <CardHeader>
                      <div className="flex items-start justify-between mb-4">
                        <motion.div
                          whileHover={{ scale: 1.1, rotate: -5 }}
                          className="p-3 bg-primary/10 rounded-sm"
                        >
                          <Icon className="h-12 w-12 text-primary" />
                        </motion.div>
                        <div className="text-right">
                          <div className="text-3xl font-black text-primary group-hover:scale-110 transition-transform">{item.stat}</div>
                          <div className="text-xs font-bold text-gray-500 uppercase tracking-wider">{item.statLabel}</div>
                        </div>
                      </div>
                      <CardTitle className="text-2xl font-black uppercase tracking-tight group-hover:text-primary transition-colors">{item.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <CardDescription className="text-base font-medium leading-relaxed">
                        {item.description}
                      </CardDescription>
                    </CardContent>
                  </Card>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Footer Section */}
      <footer className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white py-16 border-t-4 border-primary relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-transparent opacity-50" />
        <div className="relative z-10 container mx-auto px-6">
          <div className="grid md:grid-cols-3 gap-12 mb-12">
            <div>
              <h3 className="text-3xl font-black mb-6 uppercase tracking-tight bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">FindMe</h3>
              <p className="text-gray-400 font-medium leading-relaxed">
                Official missing person search platform. Authorized, secure, and reliable.
              </p>
            </div>
            <div>
              <h4 className="text-lg font-black mb-6 uppercase tracking-wider">Quick Links</h4>
              <ul className="space-y-3">
                <li>
                  <Link href="/upload" className="text-gray-400 hover:text-white hover:translate-x-2 transition-all duration-300 font-semibold uppercase text-sm tracking-wider inline-block">
                    → Upload Information
                  </Link>
                </li>
                <li>
                  <Link href="/consultation" className="text-gray-400 hover:text-white hover:translate-x-2 transition-all duration-300 font-semibold uppercase text-sm tracking-wider inline-block">
                    → Consultation & Support
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-black mb-6 uppercase tracking-wider">Emergency</h4>
              <p className="text-gray-400 font-medium mb-4">
                For immediate emergencies, contact local authorities:
              </p>
              <p className="text-2xl font-black text-red-500 hover:scale-110 transition-transform inline-block cursor-pointer">911</p>
            </div>
          </div>
          <div className="pt-8 border-t-2 border-gray-800 text-center">
            <p className="text-gray-500 font-semibold uppercase text-sm tracking-wider">
              &copy; 2024 FindMe Platform. All Rights Reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
