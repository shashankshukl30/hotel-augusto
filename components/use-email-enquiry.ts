"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { hotel } from "@/content/hotel";
import { buildEmailPayload, parseEmailResponse, type EnquiryKind, type ReplyDetails } from "@/lib/enquiry-email";

export type EmailStatus = "idle" | "pending" | "accepted" | "activation" | "error";

export function useEmailEnquiry() {
  const [status, setStatus] = useState<EmailStatus>("idle");
  const [message, setMessage] = useState("");
  const request = useRef<AbortController | null>(null);
  const revision = useRef(0);
  const reset = useCallback(() => {
    revision.current += 1;
    request.current?.abort();
    request.current = null;
    setStatus("idle");
    setMessage("");
  }, []);
  useEffect(() => () => { revision.current += 1; request.current?.abort(); }, []);

  async function submit(kind: EnquiryKind, details: Record<string, string>, reply: ReplyDetails, honey: string) {
    if (request.current) return;
    const controller = new AbortController();
    request.current = controller;
    const current = ++revision.current;
    let timedOut = false;
    const timer = window.setTimeout(() => { timedOut = true; controller.abort(); }, 20000);
    setStatus("pending");
    setMessage("");
    try {
      const body = buildEmailPayload(kind, details, reply, honey);
      const response = await fetch(`https://formsubmit.co/ajax/${hotel.email}`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(body),
        signal: controller.signal,
      });
      if (!response.ok) throw new Error("The email service is temporarily unavailable.");
      const result = parseEmailResponse(await response.json());
      if (revision.current === current) setStatus(result);
    } catch {
      if (revision.current === current) {
        setStatus("error");
        setMessage(timedOut
          ? "We could not confirm the submission in time. Your details are still here. Check with the hotel before retrying, or use WhatsApp."
          : "We could not confirm your enquiry. Your details are still here. Please try again, email the hotel or use WhatsApp.");
      }
    } finally {
      window.clearTimeout(timer);
      if (revision.current === current) request.current = null;
    }
  }
  return { status, message, pending: status === "pending", reset, submit };
}
