"use client";

import { DayPicker } from "react-day-picker";
import "react-day-picker/style.css";
import "./date-calendar.css";

function fromISO(value: string) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return undefined;
  const [year, month, day] = value.split("-").map(Number);
  const date = new Date(year, month - 1, day);
  return date.getFullYear() === year && date.getMonth() === month - 1 && date.getDate() === day
    ? date : undefined;
}

export default function DateCalendar({ value, min, label, onSelect }: {
  value: string; min: string; label: string; onSelect: (value: string) => void;
}) {
  const earliest = fromISO(min);
  const selected = fromISO(value);
  return <DayPicker mode="single" required autoFocus
    aria-label={label} selected={selected}
    defaultMonth={selected && (!earliest || selected >= earliest) ? selected : earliest}
    startMonth={earliest} disabled={earliest ? { before: earliest } : undefined}
    weekStartsOn={1} showOutsideDays fixedWeeks
    onSelect={date => onSelect(`${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`)}/>;
}
