import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildEmailPayload, parseEmailResponse, validateReplyDetails } from '../lib/enquiry-email.ts';

const reply = { email: '  guest+stay@example.com ', phone: '+91 98765 43210' };

test('email replies require a valid email and allow an omitted phone', () => {
  assert.deepEqual(validateReplyDetails(reply), {});
  assert.deepEqual(validateReplyDetails({ ...reply, phone: '' }), {});
  for (const email of ['', 'guest', 'guest@', 'guest@example', 'a b@example.com', 'guest@example.com\nBcc:other@example.com', 'a'.repeat(255) + '@example.com']) {
    assert.ok(validateReplyDetails({ ...reply, email }).email, email);
  }
  for (const phone of ['x123456', '123', '1'.repeat(31), '(......)']) {
    assert.ok(validateReplyDetails({ ...reply, phone }).phone, phone);
  }
});

test('email payload preserves guest details but prevents overrides of service fields', () => {
  const payload = buildEmailPayload('stay', {
    Name: 'Mira & Arun', Notes: 'Arrival after 6pm & vegetarian meals',
    _subject: 'Override', _cc: 'unexpected@example.com', email: 'other@example.com', recipient: 'other@example.com',
  }, reply, '');
  assert.equal(payload.Name, 'Mira & Arun');
  assert.equal(payload.Notes, 'Arrival after 6pm & vegetarian meals');
  assert.equal(payload.email, 'guest+stay@example.com');
  assert.equal(payload.phone, reply.phone);
  assert.equal(payload._subject, 'Hotel Augusto — Stay enquiry');
  assert.equal(payload._template, 'table');
  assert.equal(payload._honey, '');
  assert.equal(payload._cc, undefined);
  assert.equal(payload.recipient, undefined);
  assert.equal(buildEmailPayload('dining', {}, reply, '')._subject, 'Hotel Augusto — Dining enquiry');
  assert.equal(buildEmailPayload('group', {}, reply, '')._subject, 'Hotel Augusto — Group stay enquiry');
});

test('invalid reply details and filled honeypots never produce an email payload', () => {
  assert.throws(() => buildEmailPayload('stay', {}, { email: '', phone: '' }, ''));
  assert.throws(() => buildEmailPayload('stay', {}, reply, 'bot value'));
});

test('only explicit provider success is accepted', () => {
  assert.equal(parseEmailResponse({ success: true, message: 'The form was submitted successfully.' }), 'accepted');
  assert.equal(parseEmailResponse({ success: 'true' }), 'accepted');
  for (const response of [null, undefined, 'ok', {}, { success: false }, { success: 'false' }, { success: 1 }, { success: 'yes' }]) {
    assert.throws(() => parseEmailResponse(response));
  }
});

test('activation responses never claim email delivery or successful forwarding', () => {
  for (const message of ['Check your inbox to activate this form.', 'Please confirm your email address.', 'Email activation is required.']) {
    assert.equal(parseEmailResponse({ success: true, message }), 'activation');
    assert.equal(parseEmailResponse({ success: false, message }), 'activation');
  }
});
