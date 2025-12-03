"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { motion } from "framer-motion"
import { Phone, Mail, Heart, Shield, Users, MessageCircle, AlertCircle, Clock } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { useToast } from "@/components/ui/use-toast"
import { API_ENDPOINTS } from "@/lib/api"

const callbackSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  phone: z.string().min(10, "Valid phone number is required"),
  message: z.string().min(10, "Message must be at least 10 characters"),
})

type CallbackFormData = z.infer<typeof callbackSchema>

export default function ConsultationPage() {
  const { toast } = useToast()
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CallbackFormData>({
    resolver: zodResolver(callbackSchema),
  })

  const onSubmit = async (data: CallbackFormData) => {
    try {
      // Create FormData to send to backend
      const formDataToSend = new FormData()
      formDataToSend.append("name", data.name)
      formDataToSend.append("phone", data.phone)
      formDataToSend.append("message", data.message)

      // Send to backend API
      const response = await fetch(API_ENDPOINTS.counselor, {
        method: "POST",
        body: formDataToSend,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || "Failed to submit request")
      }

      const result = await response.json()

      toast({
        title: "Request Submitted",
        description: "We will contact you shortly. Thank you for reaching out.",
      })

      reset()
    } catch (error) {
      console.error("Counselor request error:", error)
      
      // Better error messages
      let errorMessage = "Failed to submit request. Please try again."
      
      if (error instanceof TypeError && error.message.includes("fetch")) {
        errorMessage = "Cannot connect to server. Make sure the backend is running on http://localhost:8000"
      } else if (error instanceof Error) {
        errorMessage = error.message
      }
      
      toast({
        title: "Submission Failed",
        description: errorMessage,
        variant: "destructive",
      })
    }
  }

  const contactOptions = [
    {
      title: "National Missing Person Helpline",
      phone: "1-800-843-5678",
      email: "help@missingpersons.org",
      description: "24/7 certified support line for families of missing persons",
      icon: Phone,
      badge: "24/7",
      color: "bg-primary",
    },
    {
      title: "Crisis Counselors",
      phone: "1-800-273-8255",
      email: "crisis@support.org",
      description: "Licensed mental health professionals available around the clock",
      icon: Heart,
      badge: "Certified",
      color: "bg-red-500",
    },
    {
      title: "Local Police Contact",
      phone: "911 (Emergency) or 311 (Non-Emergency)",
      email: "police@local.gov",
      description: "Immediate law enforcement response and coordination",
      icon: Shield,
      badge: "Emergency",
      color: "bg-gray-800 dark:bg-gray-700",
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#FAFAFA] via-blue-50/30 to-red-50/20 dark:from-gray-900 dark:via-blue-950/20 dark:to-gray-900 py-12 px-6">
      <div className="container mx-auto max-w-7xl">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
            className="inline-block mb-6 px-5 py-2.5 gradient-primary text-white font-bold text-sm uppercase tracking-wider shadow-lg shadow-primary/30"
          >
            <Heart className="inline h-4 w-4 mr-2" />
            Support Services
          </motion.div>
          <h1 className="text-5xl md:text-6xl font-black text-gray-900 dark:text-white mb-6 uppercase tracking-tight">
            <span className="text-gradient">Consultation & Support</span>
          </h1>
          <div className="w-24 h-1 bg-gradient-to-r from-red-500 to-red-600 mx-auto mb-6 shadow-lg"></div>
          <p className="text-xl md:text-2xl text-gray-700 dark:text-gray-300 max-w-3xl mx-auto font-bold">
            Professional support services available 24/7. You don't have to face this alone.
          </p>
        </motion.div>

        {/* Contact Options */}
        <div className="grid md:grid-cols-3 gap-6 mb-16">
          {contactOptions.map((option, index) => {
            const Icon = option.icon
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <Card className="h-full hover:shadow-2xl hover:shadow-primary/20 transition-all duration-300 border-2 border-gray-300 dark:border-gray-700 group bg-white dark:bg-gray-800">
                  <CardHeader className="border-b-2 border-gray-200 dark:border-gray-700 bg-gradient-to-r from-white to-gray-50 dark:from-gray-800 dark:to-gray-900">
                    <div className="flex items-start justify-between mb-4">
                      <motion.div
                        whileHover={{ scale: 1.1, rotate: 5 }}
                        className={`p-3 ${option.color} shadow-lg`}
                      >
                        <Icon className="h-8 w-8 text-white" />
                      </motion.div>
                      <div className={`px-3 py-1 ${option.color} text-white text-xs font-black uppercase tracking-wider shadow-md`}>
                        {option.badge}
                      </div>
                    </div>
                    <CardTitle className="text-xl font-black uppercase tracking-tight group-hover:text-primary transition-colors">{option.title}</CardTitle>
                    <CardDescription className="text-base font-semibold mt-2">{option.description}</CardDescription>
                  </CardHeader>
                  <CardContent className="p-6 bg-white dark:bg-gray-900">
                    <div className="space-y-4">
                      <div className="flex items-center space-x-3">
                        <div className="p-2 bg-gray-100 dark:bg-gray-800">
                          <Phone className="h-5 w-5 text-primary" />
                        </div>
                        <div>
                          <p className="text-xs font-black text-gray-500 uppercase tracking-wider mb-1">Phone</p>
                          <a
                            href={`tel:${option.phone}`}
                            className="text-lg font-black text-primary hover:text-primary/80 transition-colors"
                          >
                            {option.phone}
                          </a>
                        </div>
                      </div>
                      <div className="flex items-center space-x-3">
                        <div className="p-2 bg-gray-100 dark:bg-gray-800">
                          <Mail className="h-5 w-5 text-primary" />
                        </div>
                        <div>
                          <p className="text-xs font-black text-gray-500 uppercase tracking-wider mb-1">Email</p>
                          <a
                            href={`mailto:${option.email}`}
                            className="text-sm font-bold text-primary hover:text-primary/80 transition-colors break-all"
                          >
                            {option.email}
                          </a>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )
          })}
        </div>

        {/* Request Callback Form */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <Card className="shadow-2xl border-2 border-gray-300 dark:border-gray-700 max-w-3xl mx-auto bg-white dark:bg-gray-800 hover:shadow-primary/10 transition-shadow">
            <CardHeader className="border-b-2 border-gray-200 dark:border-gray-700 bg-gradient-to-r from-white to-gray-50 dark:from-gray-800 dark:to-gray-900">
              <div className="flex items-center space-x-3 mb-2">
                <motion.div
                  whileHover={{ scale: 1.1, rotate: 5 }}
                  className="p-2.5 gradient-primary shadow-lg shadow-primary/30"
                >
                  <MessageCircle className="h-6 w-6 text-white" />
                </motion.div>
                <CardTitle className="text-3xl font-black uppercase tracking-tight">Request a Callback</CardTitle>
              </div>
              <CardDescription className="text-base font-semibold">
                Fill out this form and one of our certified support specialists will contact you within 2 hours.
              </CardDescription>
            </CardHeader>
            <CardContent className="p-8 bg-white dark:bg-gray-900">
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                <div className="space-y-3">
                  <Label htmlFor="name" className="text-base font-black uppercase tracking-wide">
                    Your Name <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="name"
                    placeholder="Enter your full name"
                    {...register("name")}
                    className={errors.name ? "border-red-500 border-2" : ""}
                  />
                  {errors.name && (
                    <p className="text-sm font-bold text-red-500 uppercase text-xs tracking-wide">{errors.name.message}</p>
                  )}
                </div>

                <div className="space-y-3">
                  <Label htmlFor="phone" className="text-base font-black uppercase tracking-wide">
                    Phone Number <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="phone"
                    type="tel"
                    placeholder="Enter your phone number"
                    {...register("phone")}
                    className={errors.phone ? "border-red-500 border-2" : ""}
                  />
                  {errors.phone && (
                    <p className="text-sm font-bold text-red-500 uppercase text-xs tracking-wide">{errors.phone.message}</p>
                  )}
                </div>

                <div className="space-y-3">
                  <Label htmlFor="message" className="text-base font-black uppercase tracking-wide">
                    Message <span className="text-red-500">*</span>
                  </Label>
                  <Textarea
                    id="message"
                    placeholder="Tell us how we can help you..."
                    rows={6}
                    {...register("message")}
                    className={errors.message ? "border-red-500 border-2" : ""}
                  />
                  {errors.message && (
                    <p className="text-sm font-bold text-red-500 uppercase text-xs tracking-wide">{errors.message.message}</p>
                  )}
                </div>

                <div className="pt-4 border-t-2 border-gray-200 dark:border-gray-700">
                  <Button type="submit" className="w-full gradient-primary shadow-lg shadow-primary/30 hover:shadow-xl hover:shadow-primary/40 transition-all" size="lg">
                    Request Callback
                    <Phone className="ml-3 h-5 w-5" />
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </motion.div>

        {/* Additional Resources */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mt-16"
        >
          <Card className="bg-gradient-to-br from-primary/10 via-primary/5 to-transparent border-4 border-primary max-w-4xl mx-auto shadow-lg shadow-primary/20">
            <CardHeader className="border-b-2 border-primary/20 bg-gradient-to-r from-primary/5 to-transparent">
              <CardTitle className="flex items-center space-x-3 text-2xl font-black uppercase tracking-tight">
                <motion.div
                  whileHover={{ scale: 1.1, rotate: 5 }}
                  className="p-2 bg-primary/20"
                >
                  <Users className="h-8 w-8 text-primary" />
                </motion.div>
                <span>Additional Resources</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="p-8">
              <ul className="space-y-4 text-gray-800 dark:text-gray-200">
                {[
                  "Support groups for families of missing persons meet weekly in most major cities",
                  "Legal assistance is available for navigating the reporting process",
                  "Financial resources may be available for families in need",
                  "Media outreach support to help spread awareness",
                ].map((item, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-primary mr-4 font-black text-xl">▸</span>
                    <span className="text-base font-semibold leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}
