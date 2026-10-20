import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validateEnquiry, buildWhatsAppUrl, nextDate, stayNights } from '../lib/booking.ts';

const valid = { arrival: '2026-12-30', departure: '2027-01-02', adults: '2', children: '1', room: 'Family Room', name: 'Mira & Arun', notes: 'Arriving after 7 pm.' };
test('enquiry accepts cross-year stays and keeps all travel details in a safe WhatsApp draft', () => {
  assert.deepEqual(validateEnquiry(valid, '2026-10-19'), {});
  const link = new URL(buildWhatsAppUrl('918081709146', valid));
  assert.equal(link.hostname, 'wa.me');
  assert.equal(link.pathname, '/918081709146');
  const text = link.searchParams.get('text');
  for (const value of ['Mira & Arun', '30 Dec 2026', '2 Jan 2027', '2 adults', '1 child', 'Family Room', 'Arriving after 7 pm.']) assert.ok(text.includes(value), value);
});
test('rejects missing, impossible, past and reversed dates before a draft can open', () => {
  assert.ok(validateEnquiry({...valid, arrival: ''}, '2026-10-19').arrival);
  assert.ok(validateEnquiry({...valid, arrival: '2026-02-30'}, '2026-10-19').arrival);
  assert.ok(validateEnquiry({...valid, arrival: '2026-10-18'}, '2026-10-19').arrival);
  assert.ok(validateEnquiry({...valid, departure: valid.arrival}, '2026-10-19').departure);
  assert.ok(validateEnquiry({...valid, departure: '2026-12-29'}, '2026-10-19').departure);
});
test('validates party counts and prevents malformed external destinations', () => {
  for (const adults of ['0', '-1', '2.5', 'abc']) assert.ok(validateEnquiry({...valid, adults}, '2026-10-19').adults);
  assert.ok(validateEnquiry({...valid, children: '-1'}, '2026-10-19').children);
  assert.throws(() => buildWhatsAppUrl('javascript:alert(1)', valid));
});
test('date increment handles month ends and leap years without browser timezone conversion', () => {
  assert.equal(nextDate('2026-12-31'), '2027-01-01');
  assert.equal(nextDate('2028-02-28'), '2028-02-29');
  assert.equal(nextDate('2026-02-28'), '2026-03-01');
});
test('requested room counts validate and survive the WhatsApp enquiry', () => {
  for (const roomCount of ['0', '9', '-1', '1.5', '']) assert.ok(validateEnquiry({...valid, roomCount}, '2026-10-19').roomCount);
  assert.deepEqual(validateEnquiry({...valid, roomCount:'3'}, '2026-10-19'), {});
  assert.ok(new URL(buildWhatsAppUrl('918081709146', {...valid, roomCount:'3'})).searchParams.get('text').includes('Rooms requested: 3'));
});
test('night counts handle year boundaries, leap days and invalid ranges', () => {
  assert.equal(stayNights('2026-12-30', '2027-01-02'), 3);
  assert.equal(stayNights('2028-02-28', '2028-03-01'), 2);
  assert.equal(stayNights('2026-03-08', '2026-03-09'), 1);
  assert.equal(stayNights('', '2026-03-09'), 0);
  assert.equal(stayNights('2026-03-09', '2026-03-08'), 0);
});
