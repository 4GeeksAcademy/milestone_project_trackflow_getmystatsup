import { NextResponse } from "next/server";
import { sendPasswordResetEmail } from "@/lib/email";
import { findUserByEmail } from "@/lib/authStore";
import { createPasswordResetToken } from "@/lib/passwordReset";

type ForgotPasswordBody = {
  email?: unknown;
};

export async function POST(request: Request) {
  let email = "";

  try {
    const body = (await request.json()) as ForgotPasswordBody;
    email = typeof body.email === "string" ? body.email.trim().toLowerCase() : "";
  } catch {
    return NextResponse.json({ message: "If that address is registered, you'll receive a link shortly" }, { status: 200 });
  }

  if (email) {
    const user = findUserByEmail(email);

    if (user) {
      try {
        const token = createPasswordResetToken(user.id);
        await sendPasswordResetEmail(user.email, token);
      } catch {
        // Intentionally swallow errors to prevent account enumeration by behavior differences.
      }
    }
  }

  return NextResponse.json({ message: "If that address is registered, you'll receive a link shortly" }, { status: 200 });
}