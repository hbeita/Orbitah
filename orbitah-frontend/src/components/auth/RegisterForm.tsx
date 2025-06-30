import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/contexts/AuthContext";
import { zodResolver } from "@hookform/resolvers/zod";
import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";
import { z } from "zod";

type RegisterFormData = {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
};

interface RegisterFormProps {
  onSwitchToLogin: () => void;
}

export const RegisterForm: React.FC<RegisterFormProps> = ({
  onSwitchToLogin,
}) => {
  const { register } = useAuth();
  const { t } = useTranslation();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const registerSchema = z
    .object({
      username: z.string().min(3, t("validation.minLength", { min: 3 })),
      email: z.string().email(t("validation.email")),
      password: z.string().min(6, t("validation.minLength", { min: 6 })),
      confirmPassword: z.string(),
    })
    .refine((data) => data.password === data.confirmPassword, {
      message: t("validation.passwordMatch"),
      path: ["confirmPassword"],
    });

  const form = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
  });

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);
    setError(null);

    try {
      await register({
        username: data.username,
        email: data.email,
        password: data.password,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : t("auth.registerError"));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto bg-white/5 backdrop-blur-md border border-white/10 shadow-2xl">
      <CardHeader className="text-center">
        <div className="flex items-center justify-center space-x-2 mb-4">
          <img src="/orbitah-icon.svg" alt="Orbitah Logo" className="w-8 h-8" />
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            Orbitah
          </h1>
        </div>
        <CardTitle className="text-2xl font-bold text-white">
          {t("auth.createAccount", "Create Account")}
        </CardTitle>
        <CardDescription className="text-white/70">
          {t("auth.joinOrbitah", "Join Orbitah and start your journey")}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="username"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-white/90">
                    {t("auth.username")}
                  </FormLabel>
                  <FormControl>
                    <Input
                      placeholder={t(
                        "auth.enterUsername",
                        "Enter your username"
                      )}
                      {...field}
                      disabled={isLoading}
                      className="bg-white/10 border-white/20 text-white placeholder:text-white/50 focus:border-blue-400/50 focus:ring-blue-400/20"
                    />
                  </FormControl>
                  <FormMessage className="text-red-400" />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-white/90">
                    {t("auth.email")}
                  </FormLabel>
                  <FormControl>
                    <Input
                      type="email"
                      placeholder={t("auth.enterEmail", "Enter your email")}
                      {...field}
                      disabled={isLoading}
                      className="bg-white/10 border-white/20 text-white placeholder:text-white/50 focus:border-blue-400/50 focus:ring-blue-400/20"
                    />
                  </FormControl>
                  <FormMessage className="text-red-400" />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-white/90">
                    {t("auth.password")}
                  </FormLabel>
                  <FormControl>
                    <Input
                      type="password"
                      placeholder={t(
                        "auth.enterPassword",
                        "Enter your password"
                      )}
                      {...field}
                      disabled={isLoading}
                      className="bg-white/10 border-white/20 text-white placeholder:text-white/50 focus:border-blue-400/50 focus:ring-blue-400/20"
                    />
                  </FormControl>
                  <FormMessage className="text-red-400" />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="confirmPassword"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-white/90">
                    {t("auth.confirmPassword")}
                  </FormLabel>
                  <FormControl>
                    <Input
                      type="password"
                      placeholder={t(
                        "auth.confirmPasswordPlaceholder",
                        "Confirm your password"
                      )}
                      {...field}
                      disabled={isLoading}
                      className="bg-white/10 border-white/20 text-white placeholder:text-white/50 focus:border-blue-400/50 focus:ring-blue-400/20"
                    />
                  </FormControl>
                  <FormMessage className="text-red-400" />
                </FormItem>
              )}
            />

            {error && (
              <div className="text-sm text-red-400 bg-red-500/10 p-3 rounded-md border border-red-500/20">
                {error}
              </div>
            )}

            <Button
              type="submit"
              className="w-full bg-green-600/20 hover:bg-green-600/30 text-green-400 border border-green-500/30 transition-all duration-200"
              disabled={isLoading}
            >
              {isLoading
                ? t("auth.creatingAccount", "Creating account...")
                : t("auth.createAccount", "Create Account")}
            </Button>
          </form>
        </Form>

        <div className="mt-4 text-center">
          <p className="text-sm text-white/70">
            {t("auth.alreadyHaveAccount")}{" "}
            <button
              type="button"
              onClick={onSwitchToLogin}
              className="text-green-400 hover:text-green-300 font-medium transition-colors"
            >
              {t("auth.signIn")}
            </button>
          </p>
        </div>
      </CardContent>
    </Card>
  );
};
