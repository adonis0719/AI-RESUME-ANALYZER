import { Component, OnInit, AfterViewChecked, ElementRef, ViewChild } from '@angular/core';
import { AiChatService } from '../services/ai-chat.service';
import { marked } from 'marked';

interface ChatMessage {
  sender: 'user' | 'ai';
  text: string;
}

@Component({
  selector: 'app-ai-assistant',
  templateUrl: './ai-assistant.component.html',
  styleUrls: ['./ai-assistant.component.css']
})
export class AiAssistantComponent implements OnInit, AfterViewChecked {
  messages: ChatMessage[] = [];
  inputText = '';
  loading = false;
  private shouldScroll = false;

  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

  constructor(private aiChatService: AiChatService) {}

  ngOnInit(): void {
    this.messages.push({
      sender: 'ai',
      text: 'Hi! I\'m your AI career advisor. Ask me anything about career paths, skills, or how to improve your resume. For example: "How do I become a data scientist?" or "What skills are required for DevOps?"'
    });
  }

  ngAfterViewChecked(): void {
    if (this.shouldScroll) {
      this.scrollToBottom();
      this.shouldScroll = false;
    }
  }

  sendMessage(): void {
    const text = this.inputText.trim();
    if (!text || this.loading) return;

    this.messages.push({ sender: 'user', text });
    this.inputText = '';
    this.loading = true;
    this.shouldScroll = true;

    this.aiChatService.sendMessage(text).subscribe({
      next: (res) => {
        this.messages.push({ sender: 'ai', text: res?.reply || 'No response received.' });
        this.loading = false;
        this.shouldScroll = true;
      },
      error: (err) => {
        const msg = err?.status === 401
          ? 'Session expired. Please log in again.'
          : 'AI assistant is temporarily unavailable.';
        this.messages.push({ sender: 'ai', text: msg });
        this.loading = false;
        this.shouldScroll = true;
      }
    });
  }

  onKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  formatMessage(message: string) {
    return marked.parse(message);
  }  

  private scrollToBottom(): void {
    try {
      const el = this.messagesContainer?.nativeElement;
      if (el) {
        el.scrollTop = el.scrollHeight;
      }
    } catch {}
  }
}
