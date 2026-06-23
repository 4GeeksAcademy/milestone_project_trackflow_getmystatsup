import { NextResponse } from "next/server";
import { buildIncidentSummary } from "@/lib/incidents";

export async function GET() {
  try {
    const summary = buildIncidentSummary();
    return NextResponse.json({ data: summary }, { status: 200 });
  } catch {
    return NextResponse.json(
      { message: "Something went wrong while loading the incident summary." },
      { status: 500 },
    );
  }
}
