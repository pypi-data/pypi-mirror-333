# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.2] - 2025-03-13

- Fix bug where page titles are sometimes contained in an `a` tag
- Gracefully handle all service message, extracting group membership where possible
- Remove uniqueness constraint on messages table. It turns out that you can have duplicate Telegram message IDs within the same conversation when they are spread across multiple exported chat files.
- Store file attachments in their own database table where `file_attachments.message_id = messages.id`
- Store photo attachments in their own database table where `photo_attachments.message_id = messages.id`

## [0.0.1] - 2025-03-11

Intial release
