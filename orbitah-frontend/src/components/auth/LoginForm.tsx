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

type LoginFormData = {
  email: string;
  password: string;
};

interface LoginFormProps {
  onSwitchToRegister: () => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSwitchToRegister }) => {
  const { login } = useAuth();
  const { t } = useTranslation();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loginSchema = z.object({
    email: z.string().email(t("validation.email")),
    password: z.string().min(6, t("validation.minLength", { min: 6 })),
  });

  const form = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);
    setError(null);

    try {
      await login(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : t("auth.loginError"));
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
          {t("auth.welcomeBack", "Welcome Back")}
        </CardTitle>
        <CardDescription className="text-white/70">
          {t("auth.signInToAccount", "Sign in to your Orbitah account")}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
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

            {error && (
              <div className="text-sm text-red-400 bg-red-500/10 p-3 rounded-md border border-red-500/20">
                {error}
              </div>
            )}

            <Button
              type="submit"
              className="w-full bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 border border-blue-500/30 transition-all duration-200"
              disabled={isLoading}
            >
              {isLoading
                ? t("auth.signingIn", "Signing in...")
                : t("auth.signIn")}
            </Button>
          </form>
        </Form>

        <div className="mt-4 text-center">
          <p className="text-sm text-white/70">
            {t("auth.dontHaveAccount")}{" "}
            <button
              type="button"
              onClick={onSwitchToRegister}
              className="text-blue-400 hover:text-blue-300 font-medium transition-colors"
            >
              {t("auth.signUp")}
            </button>
          </p>
        </div>
      </CardContent>
    </Card>
  );
};
