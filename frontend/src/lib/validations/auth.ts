import * as z from 'zod';

const passwordRegex = {
  uppercase: /[A-Z]/,
  lowercase: /[a-z]/,
  number: /\d/,
  special: /[!@#$%^&*(),.?":{}|<>]/,
};

export const loginSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Invalid email address'),
  password: z
    .string()
    .min(1, 'Password is required')
    .min(8, 'Password must be at least 8 characters'),
});

export const registerSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Invalid email address'),
  password: z
    .string()
    .min(1, 'Password is required')
    .min(8, 'Password must be at least 8 characters')
    .regex(passwordRegex.uppercase, 'Password must contain at least one uppercase letter')
    .regex(passwordRegex.lowercase, 'Password must contain at least one lowercase letter')
    .regex(passwordRegex.number, 'Password must contain at least one number')
    .regex(passwordRegex.special, 'Password must contain at least one special character'),
  fullName: z
    .string()
    .min(2, 'Full name must be at least 2 characters')
    .max(100, 'Full name cannot exceed 100 characters')
    .regex(/^[a-zA-Z\s]*$/, 'Full name can only contain letters and spaces')
    .transform(val => val.trim())
    .refine(val => val.length > 0, 'Full name cannot be empty or just whitespace'),
});

export type LoginFormData = z.infer<typeof loginSchema>;
export type RegisterFormData = z.infer<typeof registerSchema>;