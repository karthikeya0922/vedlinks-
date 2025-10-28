import Link from "next/link"
import { Mail, Linkedin, Twitter } from "lucide-react"

export function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-foreground text-background border-t border-border/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-primary to-secondary rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">L</span>
              </div>
              <span className="font-bold text-lg">LearnAI</span>
            </div>
            <p className="text-background/70 text-sm">
              Transforming education through AI-powered personalized learning.
            </p>
          </div>

          {/* Product */}
          <div>
            <h3 className="font-semibold mb-4">Product</h3>
            <ul className="space-y-2 text-sm text-background/70">
              <li>
                <Link href="/features" className="hover:text-background transition-smooth">
                  Features
                </Link>
              </li>
              <li>
                <Link href="/pricing" className="hover:text-background transition-smooth">
                  Pricing
                </Link>
              </li>
              <li>
                <Link href="/teachers" className="hover:text-background transition-smooth">
                  For Teachers
                </Link>
              </li>
              <li>
                <Link href="/students" className="hover:text-background transition-smooth">
                  For Students
                </Link>
              </li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="font-semibold mb-4">Company</h3>
            <ul className="space-y-2 text-sm text-background/70">
              <li>
                <Link href="/about" className="hover:text-background transition-smooth">
                  About
                </Link>
              </li>
              <li>
                <Link href="/contact" className="hover:text-background transition-smooth">
                  Contact
                </Link>
              </li>
              <li>
                <a href="#" className="hover:text-background transition-smooth">
                  Blog
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-background transition-smooth">
                  Careers
                </a>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="font-semibold mb-4">Legal</h3>
            <ul className="space-y-2 text-sm text-background/70">
              <li>
                <a href="#" className="hover:text-background transition-smooth">
                  Privacy
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-background transition-smooth">
                  Terms
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-background transition-smooth">
                  Security
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="border-t border-background/20 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-sm text-background/70">© {currentYear} LearnAI. All rights reserved.</p>
          <div className="flex gap-4">
            <a href="#" className="text-background/70 hover:text-background transition-smooth">
              <Twitter size={20} />
            </a>
            <a href="#" className="text-background/70 hover:text-background transition-smooth">
              <Linkedin size={20} />
            </a>
            <a href="#" className="text-background/70 hover:text-background transition-smooth">
              <Mail size={20} />
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}
