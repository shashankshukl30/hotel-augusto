"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { BookingForm } from "./booking-form";

function QueryEnquiry() {
  const query = useSearchParams();
  return <BookingForm query={query.toString()}/>;
}

export function ContactEnquiry() {
  return <Suspense fallback={<BookingForm/>}><QueryEnquiry/></Suspense>;
}
