"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { motion } from "framer-motion"
import { Upload as UploadIcon, X, Loader2, AlertCircle, FileImage } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { useToast } from "@/components/ui/use-toast"

const formSchema = z.object({
  fullName: z.string().min(2, "Full name must be at least 2 characters"),
  age: z.string().min(1, "Age is required").refine((val) => !isNaN(Number(val)) && Number(val) > 0, {
    message: "Age must be a valid positive number",
  }),
  cityLastSeen: z.string().min(2, "City is required"),
  dateLastSeen: z.string().min(1, "Date is required"),
  contactPhone: z.string().min(10, "Valid phone number is required"),
  nearbyPoliceStation: z.string().min(2, "Police station name and address is required"),
  additionalDescription: z.string().optional(),
})

type FormData = z.infer<typeof formSchema>

export default function UploadPage() {
  const [imagePreviews, setImagePreviews] = useState<string[]>([])
  const [isUploading, setIsUploading] = useState(false)
  const { toast } = useToast()

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
  })

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    
    if (files.length === 0) return

    // Check total number of images (max 10)
    if (imagePreviews.length + files.length > 10) {
      toast({
        title: "Too many images",
        description: "You can upload a maximum of 10 images",
        variant: "destructive",
      })
      return
    }

    const validFiles: File[] = []
    const invalidFiles: string[] = []

    files.forEach((file) => {
      if (file.size > 5 * 1024 * 1024) {
        invalidFiles.push(file.name)
      } else if (!file.type.startsWith('image/')) {
        invalidFiles.push(file.name)
      } else {
        validFiles.push(file)
      }
    })

    if (invalidFiles.length > 0) {
      toast({
        title: "Invalid files",
        description: `${invalidFiles.length} file(s) were rejected. Please upload images smaller than 5MB.`,
        variant: "destructive",
      })
    }

    if (validFiles.length === 0) return

    // Read all valid files
    const readers = validFiles.map((file) => {
      return new Promise<string>((resolve, reject) => {
        const reader = new FileReader()
        reader.onloadend = () => {
          resolve(reader.result as string)
        }
        reader.onerror = reject
        reader.readAsDataURL(file)
      })
    })

    Promise.all(readers)
      .then((previews) => {
        setImagePreviews((prev) => [...prev, ...previews])
        toast({
          title: "Images added",
          description: `${validFiles.length} image(s) added successfully`,
        })
      })
      .catch(() => {
        toast({
          title: "Error",
          description: "Failed to read some images",
          variant: "destructive",
        })
      })

    // Reset input to allow selecting the same file again
    e.target.value = ''
  }

  const removeImage = (index: number) => {
    setImagePreviews((prev) => prev.filter((_, i) => i !== index))
  }

  const removeAllImages = () => {
    setImagePreviews([])
  }

  const onSubmit = async (data: FormData) => {
    setIsUploading(true)
    
    // Simulate upload delay
    await new Promise((resolve) => setTimeout(resolve, 1500))

    const formData = {
      ...data,
      imagePreviews,
    }

    console.log("Form submitted:", formData)

    setIsUploading(false)
    
    toast({
      title: "Submission Successful",
      description: `Your information with ${imagePreviews.length} image(s) has been submitted. We will process it shortly. If any lead is found, we will contact the nearby police station you provided for immediate action.`,
      duration: 8000,
    })

    reset()
    setImagePreviews([])
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#FAFAFA] via-blue-50/30 to-red-50/20 dark:from-gray-900 dark:via-blue-950/20 dark:to-gray-900 py-12 px-6">
      <div className="container mx-auto max-w-3xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-8"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
            className="inline-block mb-4 px-5 py-2.5 bg-gradient-to-r from-red-500 to-red-600 text-white font-bold text-sm uppercase tracking-wider shadow-lg shadow-red-500/30"
          >
            <AlertCircle className="inline h-4 w-4 mr-2" />
            ⚠️ Hackathon Submission - ARM AI Challenge
          </motion.div>
          <h1 className="text-5xl md:text-6xl font-black text-gray-900 dark:text-white mb-4 uppercase tracking-tight">
            <span className="text-gradient">Report Missing Person</span>
          </h1>
          <p className="text-xl font-bold text-gray-700 dark:text-gray-300">
            Submit verified information through our secure platform
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          <Card className="shadow-2xl border-2 border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 hover:shadow-primary/10 transition-shadow">
            <CardHeader className="border-b-2 border-gray-200 dark:border-gray-700 bg-gradient-to-r from-white to-gray-50 dark:from-gray-800 dark:to-gray-900">
              <CardTitle className="text-3xl font-black uppercase tracking-tight">Information Form</CardTitle>
              <CardDescription className="text-base font-semibold mt-2">
                All fields marked with <span className="text-red-500 font-black">*</span> are required. Information is encrypted and secure.
              </CardDescription>
            </CardHeader>
            <CardContent className="p-8 bg-white dark:bg-gray-900">
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
                {/* Full Name */}
                <div className="space-y-3">
                  <Label htmlFor="fullName" className="text-base font-black uppercase tracking-wide">
                    Full Name <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="fullName"
                    placeholder="Enter full legal name"
                    {...register("fullName")}
                    className={errors.fullName ? "border-red-500 border-2" : ""}
                  />
                  {errors.fullName && (
                    <p className="text-sm font-bold text-red-500 uppercase text-xs tracking-wide">{errors.fullName.message}</p>
                  )}
                </div>

                {/* Age */}
                <div className="space-y-3">
                  <Label htmlFor="age" className="text-base font-black uppercase tracking-wide">
                    Age <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="age"
                    type="number"
                    placeholder="Enter age"
                    {...register("age")}
                    className={errors.age ? "border-red-500 border-2" : ""}
                  />
                  {errors.age && (
                    <p className="text-sm font-bold text-red-500 uppercase text-xs tracking-wide">{errors.age.message}</p>
                  )}
                </div>

                {/* City Last Seen */}
                <div className="space-y-3">
                  <Label htmlFor="cityLastSeen" className="text-base font-black uppercase tracking-wide">
                    City Last Seen <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="cityLastSeen"
                    placeholder="Enter city name"
                    {...register("cityLastSeen")}
                    className={errors.cityLastSeen ? "border-red-500 border-2" : ""}
                  />
                  {errors.cityLastSeen && (
                    <p className="text-sm font-bold text-red-500 uppercase text-xs tracking-wide">{errors.cityLastSeen.message}</p>
                  )}
                </div>

                {/* Date Last Seen */}
                <div className="space-y-3">
                  <Label htmlFor="dateLastSeen" className="text-base font-black uppercase tracking-wide">
                    Date Last Seen <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="dateLastSeen"
                    type="date"
                    {...register("dateLastSeen")}
                    className={errors.dateLastSeen ? "border-red-500 border-2" : ""}
                  />
                  {errors.dateLastSeen && (
                    <p className="text-sm font-bold text-red-500 uppercase text-xs tracking-wide">{errors.dateLastSeen.message}</p>
                  )}
                </div>

                {/* Contact Phone */}
                <div className="space-y-3">
                  <Label htmlFor="contactPhone" className="text-base font-black uppercase tracking-wide">
                    Contact Phone Number <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="contactPhone"
                    type="tel"
                    placeholder="Enter phone number"
                    {...register("contactPhone")}
                    className={errors.contactPhone ? "border-red-500 border-2" : ""}
                  />
                  {errors.contactPhone && (
                    <p className="text-sm font-bold text-red-500 uppercase text-xs tracking-wide">{errors.contactPhone.message}</p>
                  )}
                </div>

                {/* Nearby Police Station */}
                <div className="space-y-3">
                  <Label htmlFor="nearbyPoliceStation" className="text-base font-black uppercase tracking-wide">
                    Nearby Police Station Name & Address <span className="text-red-500">*</span>
                  </Label>
                  <Textarea
                    id="nearbyPoliceStation"
                    placeholder="Enter police station name and full address"
                    rows={3}
                    {...register("nearbyPoliceStation")}
                    className={errors.nearbyPoliceStation ? "border-red-500 border-2" : ""}
                  />
                  {errors.nearbyPoliceStation && (
                    <p className="text-sm font-bold text-red-500 uppercase text-xs tracking-wide">{errors.nearbyPoliceStation.message}</p>
                  )}
                  <p className="text-sm font-semibold text-gray-600 dark:text-gray-400 italic">
                    📍 Report the case to the nearby police station as well. This information will be used to coordinate with local authorities.
                  </p>
                </div>

                {/* Additional Description */}
                <div className="space-y-3">
                  <Label htmlFor="additionalDescription" className="text-base font-black uppercase tracking-wide">
                    Additional Description
                  </Label>
                  <Textarea
                    id="additionalDescription"
                    placeholder="Any additional information that might help (clothing, distinguishing features, last known location details, etc.)"
                    rows={5}
                    {...register("additionalDescription")}
                  />
                </div>

                {/* Image Upload */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="image" className="text-base font-black uppercase tracking-wide">
                      Upload Photos <span className="text-red-500">*</span>
                    </Label>
                    {imagePreviews.length > 0 && (
                      <button
                        type="button"
                        onClick={removeAllImages}
                        className="text-sm font-bold text-red-500 hover:text-red-600 uppercase tracking-wide transition-colors"
                      >
                        Remove All
                      </button>
                    )}
                  </div>
                  
                  {imagePreviews.length === 0 ? (
                    <div className="border-4 border-dashed border-gray-400 dark:border-gray-600 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 p-12 text-center hover:border-primary hover:bg-gradient-to-br hover:from-primary/5 hover:to-primary/10 transition-all duration-300 group">
                      <input
                        type="file"
                        id="image"
                        accept="image/*"
                        multiple
                        onChange={handleImageChange}
                        className="hidden"
                      />
                      <label
                        htmlFor="image"
                        className="cursor-pointer flex flex-col items-center"
                      >
                        <motion.div
                          whileHover={{ scale: 1.1, rotate: 5 }}
                          className="p-4 gradient-primary mb-4 shadow-lg shadow-primary/30 group-hover:shadow-xl group-hover:shadow-primary/40 transition-shadow"
                        >
                          <FileImage className="h-12 w-12 text-white" />
                        </motion.div>
                        <p className="text-base font-bold text-gray-700 dark:text-gray-300 uppercase tracking-wide mb-2 group-hover:text-primary transition-colors">
                          Click to upload or drag and drop
                        </p>
                        <p className="text-sm font-semibold text-gray-500 uppercase text-xs tracking-wider">
                          PNG, JPG, GIF up to 5MB each (Max 10 images)
                        </p>
                      </label>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {/* Image Grid */}
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                        {imagePreviews.map((preview, index) => (
                          <motion.div
                            key={index}
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: index * 0.1 }}
                            className="relative group aspect-square border-2 border-gray-300 dark:border-gray-700 overflow-hidden bg-gray-100 dark:bg-gray-800 rounded-lg"
                          >
                            <img
                              src={preview}
                              alt={`Preview ${index + 1}`}
                              className="w-full h-full object-cover"
                            />
                            <button
                              type="button"
                              onClick={() => removeImage(index)}
                              className="absolute top-2 right-2 bg-red-500 text-white p-2 hover:bg-red-600 transition-colors border-2 border-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                            >
                              <X className="h-4 w-4" />
                            </button>
                            <div className="absolute bottom-2 left-2 bg-black/50 text-white text-xs font-bold px-2 py-1 rounded">
                              {index + 1}
                            </div>
                          </motion.div>
                        ))}
                      </div>
                      
                      {/* Add More Images Button */}
                      {imagePreviews.length < 10 && (
                        <div className="border-2 border-dashed border-gray-400 dark:border-gray-600 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 p-6 text-center hover:border-primary hover:bg-gradient-to-br hover:from-primary/5 hover:to-primary/10 transition-all duration-300 group cursor-pointer">
                          <input
                            type="file"
                            id="image-add"
                            accept="image/*"
                            multiple
                            onChange={handleImageChange}
                            className="hidden"
                          />
                          <label
                            htmlFor="image-add"
                            className="cursor-pointer flex flex-col items-center"
                          >
                            <motion.div
                              whileHover={{ scale: 1.1, rotate: 5 }}
                              className="p-3 gradient-primary mb-2 shadow-lg shadow-primary/30 group-hover:shadow-xl group-hover:shadow-primary/40 transition-shadow"
                            >
                              <UploadIcon className="h-6 w-6 text-white" />
                            </motion.div>
                            <p className="text-sm font-bold text-gray-700 dark:text-gray-300 uppercase tracking-wide group-hover:text-primary transition-colors">
                              Add More Images ({imagePreviews.length}/10)
                            </p>
                          </label>
                        </div>
                      )}
                      
                      {isUploading && (
                        <div className="absolute inset-0 bg-black/70 flex items-center justify-center z-50">
                          <div className="bg-white p-6 border-4 border-primary">
                            <Loader2 className="h-8 w-8 text-primary animate-spin mx-auto" />
                            <p className="mt-4 font-bold text-gray-900 uppercase tracking-wide">Processing...</p>
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Submit Button */}
                <div className="pt-4 border-t-2 border-gray-200 dark:border-gray-700">
                  <Button
                    type="submit"
                    className="w-full gradient-primary shadow-lg shadow-primary/30 hover:shadow-xl hover:shadow-primary/40 transition-all"
                    size="lg"
                    disabled={isUploading || imagePreviews.length === 0}
                  >
                    {isUploading ? (
                      <>
                        <Loader2 className="mr-3 h-5 w-5 animate-spin" />
                        Processing Submission...
                      </>
                    ) : (
                      <>
                        Submit Information
                        <UploadIcon className="ml-3 h-5 w-5" />
                      </>
                    )}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}
