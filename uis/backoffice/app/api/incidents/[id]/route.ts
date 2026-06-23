import { NextResponse } from "next/server";
import { getIncidentById } from "@/lib/incidents";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await params;
    const incident = getIncidentById(id);

    if (!incident) {
      return NextResponse.json(
        { message: "Incident not found." },
        { status: 404 },
      );
    }

    return NextResponse.json({ data: incident }, { status: 200 });
  } catch {
    return NextResponse.json(
      { message: "Something went wrong while fetching the incident." },
      { status: 500 },
    );
  }
}
