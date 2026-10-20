"use client";

import { lazy, Suspense, useEffect, useRef, useState, type ComponentProps } from "react";
import { CalendarDays, X } from "lucide-react";
import { localToday } from "@/lib/booking";
import "./date-field.css";

const DateCalendar = lazy(() => import("./date-calendar"));
type Props = Omit<ComponentProps<"input">, "type" | "value" | "defaultValue" | "onChange"> & {
  label: string;
  value: string;
  onValueChange: (value: string) => void;
  minToday?: boolean;
};

/** Native form values and keyboard editing, with one consistent touch calendar. */
export function DateField({ label, value, onValueChange, minToday = false, min,
  id, onFocus, className = "", ...props }: Props) {
  const input = useRef<HTMLInputElement>(null);
  const dialog = useRef<HTMLDialogElement>(null);
  const opener = useRef<HTMLElement | null>(null);
  const backdropPress = useRef(false);
  const openingPress = useRef(false);
  const [open, setOpen] = useState(false);
  const [calendarMin, setCalendarMin] = useState("");
  const calendarId = `${id}-calendar`;
  const titleId = `${id}-calendar-title`;

  useEffect(() => {
    const element = dialog.current;
    if (!element) return;
    if (open && !element.open) element.showModal();
    else if (!open && element.open) element.close();
  }, [open]);

  function showCalendar(target: HTMLElement, duringPointerDown = false) {
    opener.current = target;
    backdropPress.current = false;
    openingPress.current = duringPointerDown;
    const earliest = minToday ? localToday() : String(min || "");
    setCalendarMin(earliest);
    if (input.current) input.current.min = earliest;
    setOpen(true);
  }

  return <div className="date-control" data-empty={!value}>
    <input {...props} ref={input} id={id} className={`date-input ${className}`}
      type="date" value={value} min={min} placeholder="YYYY-MM-DD"
      aria-haspopup="dialog" aria-controls={calendarId}
      onFocus={event => {
        if (minToday) event.currentTarget.min = localToday();
        onFocus?.(event);
      }}
      onChange={event => onValueChange(event.target.value)}
      onPointerDown={event => {
        // Native date segments can consume clicks before React receives them.
        // Own the primary pointer gesture before the OS control handles it.
        if (event.button === 0) {
          event.preventDefault();
          showCalendar(event.currentTarget, true);
        }
      }}
      onClick={event => { event.preventDefault(); showCalendar(event.currentTarget); }}
      onKeyDown={event => {
        if (event.key === "Enter" || event.key === " " || (event.altKey && event.key === "ArrowDown")) {
          event.preventDefault();
          showCalendar(event.currentTarget);
        }
      }}/>
    {!value && <span className="date-field-placeholder" aria-hidden="true">Choose date</span>}
    <button type="button" className="date-picker-trigger" aria-label={`Open ${label.toLowerCase()} calendar`}
      aria-haspopup="dialog" aria-expanded={open} aria-controls={calendarId}
      style={{ color: "var(--ink)" }} onClick={event => showCalendar(event.currentTarget)}>
      <CalendarDays size={18} aria-hidden="true"/>
    </button>
    <dialog ref={dialog} id={calendarId} className="date-picker-dialog" aria-labelledby={titleId}
      onClose={() => {
        setOpen(false);
        opener.current?.focus({ preventScroll: true });
      }}
      onPointerDown={event => {
        // A fresh gesture inside the calendar is intentional. The gesture
        // that opened it started on the input, outside this dialog.
        openingPress.current = false;
        const box = event.currentTarget.getBoundingClientRect();
        backdropPress.current = event.target === event.currentTarget &&
          (event.clientX < box.left || event.clientX > box.right ||
            event.clientY < box.top || event.clientY > box.bottom);
      }}
      onKeyDownCapture={() => { openingPress.current = false; }}
      onClickCapture={event => {
        // WebKit can retarget the opening touch to a loaded day button.
        // Consume that click before it reaches any calendar action.
        if (openingPress.current && event.detail > 0) {
          event.preventDefault();
          event.stopPropagation();
        }
        openingPress.current = false;
      }}
      onClick={event => {
        // An opening touch can finish on the newly shown backdrop. Only a
        // gesture that also started there should dismiss the calendar.
        if (backdropPress.current && event.target === event.currentTarget) event.currentTarget.close();
        backdropPress.current = false;
      }}>
      <div className="date-picker-heading"><h2 id={titleId}>{label}</h2>
        <button type="button" className="date-picker-close" aria-label="Close calendar"
          style={{ color: "var(--ink)" }} onClick={() => dialog.current?.close()}><X size={21}/></button>
      </div>
      {open && <Suspense fallback={<p className="date-picker-loading" role="status">Loading calendar…</p>}>
        <DateCalendar value={value} min={calendarMin} label={label} onSelect={date => {
          onValueChange(date);
          dialog.current?.close();
        }}/>
      </Suspense>}
    </dialog>
  </div>;
}
