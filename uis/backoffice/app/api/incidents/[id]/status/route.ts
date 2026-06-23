import { NextResponse } from "next/server";
import {
  getApiErrorBody,
  updateIncidentStatus,
  validateStatusPatch,
} from "@/lib/incidents";

export async function PATCH(
  request: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await params;
    const body = await request.json();
    const validation = validateStatusPatch(body);

    if (validation.errors.length > 0 || !validation.data) {
      return NextResponse.json(getApiErrorBody(validation.errors[0]), { status: 400 });
    }

    const result = updateIncidentStatus(id, validation.data.status);

    if (!result) {
      return NextResponse.json({ message: "Incident not found." }, { status: 404 });
    }

    if (result.error) {
      return NextResponse.json(getApiErrorBody(result.error), { status: 400 });
    }

    return NextResponse.json({ data: result.incident }, { status: 200 });
  } catch {
    return NextResponse.json(
      { message: "Something went wrong while updating incident status." },
      { status: 500 },
    );
  }
}
