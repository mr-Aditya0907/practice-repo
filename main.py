#!/usr/bin/env python3
"""
Main entry point for Personal AI Assistant
"""
import sys
from colorama import Fore, Style, init
from core.ai_assistant import AIAssistant
from utils.logger import get_logger

# Initialize colorama for colored output
init(autoreset=True)

logger = get_logger(__name__)

def print_welcome():
    """Print welcome message"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}🤖 Personal AI Assistant - Multilingual Chatbot")
    print(f"{Fore.CYAN}{'='*60}\n")
    print(f"{Fore.YELLOW}Commands:")
    print(f"  {Fore.GREEN}help{Fore.YELLOW} - Show available commands")
    print(f"  {Fore.GREEN}providers{Fore.YELLOW} - List available AI providers")
    print(f"  {Fore.GREEN}use <provider>{Fore.YELLOW} - Switch to specific provider")
    print(f"  {Fore.GREEN}all{Fore.YELLOW} - Get responses from all providers")
    print(f"  {Fore.GREEN}history{Fore.YELLOW} - Show conversation history")
    print(f"  {Fore.GREEN}clear{Fore.YELLOW} - Clear conversation history")
    print(f"  {Fore.GREEN}summary{Fore.YELLOW} - Show conversation summary")
    print(f"  {Fore.GREEN}exit{Fore.YELLOW} - Exit the application\n")

def print_help():
    """Print help information"""
    print(f"\n{Fore.CYAN}Available Commands:")
    print(f"  {Fore.GREEN}help{Fore.RESET} - Show this help message")
    print(f"  {Fore.GREEN}providers{Fore.RESET} - Show available AI providers")
    print(f"  {Fore.GREEN}use <provider>{Fore.RESET} - Switch provider (openai, gemini, groq, huggingface)")
    print(f"  {Fore.GREEN}all{Fore.RESET} - Get responses from all available providers")
    print(f"  {Fore.GREEN}history{Fore.RESET} - Show last 5 messages")
    print(f"  {Fore.GREEN}clear{Fore.RESET} - Clear conversation history")
    print(f"  {Fore.GREEN}summary{Fore.RESET} - Show conversation summary")
    print(f"  {Fore.GREEN}exit{Fore.RESET} - Exit the application")
    print(f"  {Fore.GREEN}Any other text{Fore.RESET} - Chat with the AI\n")

def show_providers(assistant):
    """Show available providers"""
    available = assistant.get_available_providers()
    print(f"\n{Fore.CYAN}Available AI Providers:")
    
    if available:
        for provider in available:
            status = "✓ (Current)" if provider == assistant.current_provider else "✓"
            print(f"  {Fore.GREEN}{status}{Fore.RESET} {provider}")
    else:
        print(f"  {Fore.RED}No providers configured!{Fore.RESET}")
        print(f"  {Fore.YELLOW}Please add API keys to .env file\n")

def show_history(assistant):
    """Show conversation history"""
    history = assistant.get_history()
    
    if not history:
        print(f"\n{Fore.YELLOW}No conversation history\n")
        return
    
    print(f"\n{Fore.CYAN}Conversation History (Last 5):")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    for i, msg in enumerate(history[-5:], 1):
        print(f"{Fore.GREEN}[{i}] User:{Fore.RESET} {msg['user'][:100]}...")
        print(f"{Fore.BLUE}    Response ({msg['provider']}):{Fore.RESET} {msg['assistant'][:100]}...")
        print()

def process_command(command, assistant):
    """
    Process special commands
    
    Args:
        command (str): User command
        assistant (AIAssistant): AI Assistant instance
        
    Returns:
        bool: True if command was processed, False otherwise
    """
    command = command.lower().strip()
    
    if command == 'help':
        print_help()
        return True
    
    elif command == 'providers':
        show_providers(assistant)
        return True
    
    elif command.startswith('use '):
        provider = command.replace('use ', '').strip()
        if assistant.set_provider(provider):
            print(f"\n{Fore.GREEN}✓ Switched to {provider}{Fore.RESET}\n")
        else:
            print(f"\n{Fore.RED}✗ Failed to switch provider{Fore.RESET}\n")
        return True
    
    elif command == 'all':
        return False  # Process as regular message to trigger all providers
    
    elif command == 'history':
        show_history(assistant)
        return True
    
    elif command == 'clear':
        assistant.clear_history()
        print(f"\n{Fore.GREEN}✓ Conversation history cleared{Fore.RESET}\n")
        return True
    
    elif command == 'summary':
        summary = assistant.get_conversation_summary()
        print(f"\n{Fore.CYAN}Conversation Summary:")
        print(f"{Fore.CYAN}{'='*60}")
        print(summary)
        print(f"{Fore.CYAN}{'='*60}\n")
        return True
    
    elif command == 'exit':
        print(f"\n{Fore.CYAN}Goodbye! 👋\n")
        sys.exit(0)
    
    return False

def main():
    """Main function"""
    try:
        # Initialize assistant
        assistant = AIAssistant()
        
        # Check if any providers are available
        if not assistant.get_available_providers():
            print(f"\n{Fore.RED}❌ No AI providers configured!{Fore.RESET}")
            print(f"{Fore.YELLOW}Please add your API keys to .env file:")
            print(f"  1. Copy .env.example to .env")
            print(f"  2. Add your API keys")
            print(f"  3. Run this script again\n")
            return
        
        print_welcome()
        
        # Main conversation loop
        while True:
            try:
                user_input = input(f"{Fore.GREEN}You: {Fore.RESET}").strip()
                
                if not user_input:
                    continue
                
                # Check if it's a command
                if process_command(user_input, assistant):
                    continue
                
                # Handle 'all' command specially
                if user_input.lower() == 'all':
                    print(f"\n{Fore.CYAN}Getting responses from all providers...\n")
                    responses = assistant.chat_with_all_providers(
                        input(f"{Fore.GREEN}Enter your message: {Fore.RESET}").strip()
                    )
                    
                    for provider, response in responses.items():
                        print(f"\n{Fore.BLUE}[{provider.upper()}]{Fore.RESET}")
                        print(f"{Fore.YELLOW}Language: {response['language']}{Fore.RESET}")
                        print(f"{Fore.GREEN}{response['content']}\n")
                    continue
                
                # Regular chat
                print(f"\n{Fore.CYAN}Assistant: {Fore.RESET}Thinking...\n")
                response = assistant.chat(user_input)
                
                if response['error']:
                    print(f"{Fore.RED}{response['content']}\n")
                else:
                    print(f"{Fore.YELLOW}Language: {response['language']}")
                    print(f"{Fore.BLUE}Provider: {response['provider']}{Fore.RESET}")
                    print(f"{Fore.GREEN}{response['content']}\n")
            
            except KeyboardInterrupt:
                print(f"\n\n{Fore.CYAN}Goodbye! 👋\n")
                break
            except Exception as e:
                logger.error(f"Error in conversation loop: {e}")
                print(f"{Fore.RED}An error occurred: {e}\n{Fore.RESET}")
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"{Fore.RED}Fatal error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
