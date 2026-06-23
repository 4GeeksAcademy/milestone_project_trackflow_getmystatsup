import { NextResponse } from "next/server";
import {
  createIncident,
  getApiErrorBody,
  listIncidents,
  parseIncidentFilters,
  validateCreateInput,
} from "@/lib/incidents";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const validation = validateCreateInput(body);

    if (validation.errors.length > 0 || !validation.data) {
      return NextResponse.json(getApiErrorBody(validation.errors[0]), { status: 400 });
    }

    const incident = createIncident(validation.data);

    return NextResponse.json({ data: incident }, { status: 201 });
  } catch {
    return NextResponse.json(
      { message: "Something went wrong while creating the incident." },
      { status: 500 },
    );
  }
}

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const parsed = parseIncidentFilters(searchParams);

    if (parsed.errors.length > 0 || !parsed.filters) {
      return NextResponse.json(getApiErrorBody(parsed.errors[0]), { status: 400 });
    }

    const incidents = listIncidents(parsed.filters);

    return NextResponse.json({ data: incidents }, { status: 200 });
  } catch {
    return NextResponse.json(
      { message: "Something went wrong while listing incidents." },
      { status: 500 },
    );
  }
}
