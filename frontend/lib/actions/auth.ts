'use server';
export const dynamic = 'force-dynamic';
export const revalidate = 0;

import { signIn } from '@/auth';
import { AuthError } from 'next-auth';
import { redirect } from 'next/navigation';

// export async function authenticate(
//   prevState: string | undefined,
//   formData: FormData
// ) {
//   try {
//     await signIn("credentials", formData);
//   } catch (error) {
//     if (error instanceof AuthError) {
//       switch (error.type) {
//         case "CredentialsSignin":
//           return "Invalid credentials.";
//         default:
//           return "Something went wrong.";
//       }
//     }
//     throw error;
//   }
// }
export async function authenticate(
  prevState: string | undefined,
  formData: FormData,
) {
  console.log('auth.ts: Starting authentication process');
  try {
    const email = formData.get('email') as string;
    const password = formData.get('password') as string;

    console.log('auth.ts: Form data:', {
      email,
      hasPassword: !!password,
    });

    console.log('auth.ts: Calling signIn');
    const result = await signIn('credentials', {
      email,
      password,
      redirect: false,
    });

    console.log('auth.ts: SignIn result:', result);

    if (result?.error) {
      return result.error;
    }

    if (result?.url) {
      redirect(result.url);
    }
  } catch (error: unknown) {
    console.error('auth.ts: Authentication error:', {
      name: error instanceof Error ? error.name : 'Unknown',
      message: error instanceof Error ? error.message : String(error),
      stack: error instanceof Error ? error.stack : undefined,
    });

    if (error instanceof AuthError) {
      console.log('auth.ts: AuthError type:', error.type);
      switch (error.type) {
        case 'CredentialsSignin':
          return 'Invalid credentials.';
        default:
          return 'Something went wrong.';
      }
    }
    return 'An unexpected error occurred.';
  }
} 