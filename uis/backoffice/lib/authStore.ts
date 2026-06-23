import bcrypt from "bcryptjs";

type UserRecord = {
  id: string;
  email: string;
  passwordHash: string;
};

type ResetTokenRecord = {
  userId: string;
  expiresAt: number;
};

const usersByEmail = new Map<string, UserRecord>();
const usersById = new Map<string, UserRecord>();
const resetTokensByJti = new Map<string, ResetTokenRecord>();

const defaultDemoEmail = process.env.AUTH_DEMO_USER_EMAIL?.trim().toLowerCase() || "demo@trackflow.local";
const defaultDemoPassword = process.env.AUTH_DEMO_USER_PASSWORD || "ChangeMe123!";
const demoPasswordHash = bcrypt.hashSync(defaultDemoPassword, 12);

const demoUser: UserRecord = {
  id: "user_demo_1",
  email: defaultDemoEmail,
  passwordHash: demoPasswordHash,
};

usersByEmail.set(demoUser.email, demoUser);
usersById.set(demoUser.id, demoUser);

export function findUserByEmail(email: string): UserRecord | null {
  return usersByEmail.get(email.trim().toLowerCase()) || null;
}

export function findUserById(userId: string): UserRecord | null {
  return usersById.get(userId) || null;
}

export function updateUserPassword(userId: string, passwordHash: string): boolean {
  const user = usersById.get(userId);
  if (!user) {
    return false;
  }

  const nextUser: UserRecord = {
    ...user,
    passwordHash,
  };

  usersById.set(nextUser.id, nextUser);
  usersByEmail.set(nextUser.email, nextUser);
  return true;
}

export function saveResetToken(jti: string, userId: string, expiresAt: number): void {
  resetTokensByJti.set(jti, { userId, expiresAt });
}

export function isResetTokenActive(jti: string, userId: string): boolean {
  const tokenRecord = resetTokensByJti.get(jti);

  if (!tokenRecord) {
    return false;
  }

  if (tokenRecord.userId !== userId) {
    return false;
  }

  if (Date.now() >= tokenRecord.expiresAt) {
    resetTokensByJti.delete(jti);
    return false;
  }

  return true;
}

export function consumeResetToken(jti: string, userId: string): boolean {
  const tokenRecord = resetTokensByJti.get(jti);

  if (!tokenRecord || tokenRecord.userId !== userId) {
    return false;
  }

  if (Date.now() >= tokenRecord.expiresAt) {
    resetTokensByJti.delete(jti);
    return false;
  }

  resetTokensByJti.delete(jti);
  return true;
}