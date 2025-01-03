import { useState } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'react-hot-toast';
import { useAuth } from '@/hooks/useAuth';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { registerSchema, type RegisterFormData } from '@/lib/validations/auth';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { FormMessage } from '@/components/ui/form';

export function RegisterForm() {
  const router = useRouter();
  const { register: registerUser } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      email: '',
      password: '',
      fullName: '',
    },
  });

  async function onSubmit(data: RegisterFormData) {
    setIsLoading(true);

    try {
      await registerUser(data.email, data.password, data.fullName);
      toast.success('Registration successful! Please log in.');
      router.push('/login');
    } catch (error) {
      if (error instanceof Error) {
        toast.error(error.message);
      } else {
        toast.error('Registration failed. Please try again.');
      }
      console.error('Registration error:', error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="space-y-2">
        <label
          htmlFor="fullName"
          className="block text-sm font-medium text-gray-700 dark:text-gray-200"
        >
          Full Name
        </label>
        <Input
          id="fullName"
          type="text"
          placeholder="Enter your full name"
          disabled={isLoading}
          {...register('fullName')}
          aria-invalid={!!errors.fullName}
        />
        {errors.fullName && (
          <FormMessage>{errors.fullName.message}</FormMessage>
        )}
      </div>

      <div className="space-y-2">
        <label
          htmlFor="email"
          className="block text-sm font-medium text-gray-700 dark:text-gray-200"
        >
          Email address
        </label>
        <Input
          id="email"
          type="email"
          placeholder="Enter your email"
          autoComplete="email"
          disabled={isLoading}
          {...register('email')}
          aria-invalid={!!errors.email}
        />
        {errors.email && (
          <FormMessage>{errors.email.message}</FormMessage>
        )}
      </div>

      <div className="space-y-2">
        <label
          htmlFor="password"
          className="block text-sm font-medium text-gray-700 dark:text-gray-200"
        >
          Password
        </label>
        <Input
          id="password"
          type="password"
          placeholder="Create a password"
          autoComplete="new-password"
          disabled={isLoading}
          {...register('password')}
          aria-invalid={!!errors.password}
        />
        {errors.password && (
          <FormMessage>{errors.password.message}</FormMessage>
        )}
      </div>

      <Button
        type="submit"
        className="w-full"
        disabled={isLoading}
      >
        {isLoading ? 'Creating account...' : 'Create account'}
      </Button>
    </form>
  );
}