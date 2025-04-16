import streamlit as st
import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os
import atexit

def apply_custom_css():
    custom_css = """
    <style>
        /* Modern CSS Reset and Base Styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html {
            scroll-behavior: smooth;
        }
        
        /* Advanced Variable System */
        :root {
            --primary-gradient: linear-gradient(-45deg, #0f2027, #203a43, #1a2a6c, #2c3e50);
            --accent-gradient: linear-gradient(45deg, #833ab4, #fd1d1d, #fcb045);
            --text-gradient: linear-gradient(90deg, #f8f9fa, #00dbde, #fc00ff, #f8f9fa);
            --glass-bg: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
            --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            --primary-text: #f8f9fa;
            --secondary-text: rgba(255, 255, 255, 0.7);
            --accent-color: #64ffda;
            --card-bg: rgba(20, 30, 48, 0.7);
            --card-hover-bg: rgba(30, 40, 58, 0.8);
            --shadow-sm: 0 5px 10px rgba(0, 0, 0, 0.2);
            --shadow-md: 0 10px 20px rgba(0, 0, 0, 0.3);
            --shadow-lg: 0 15px 35px rgba(0, 0, 0, 0.3);
            --rounded-sm: 10px;
            --rounded-md: 15px;
            --rounded-lg: 20px;
            --rounded-full: 50px;
            --transition-fast: 0.3s ease;
            --transition-normal: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            --transition-bounce: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        
        /* General Styles with Advanced Gradient */
        body {
            font-family: 'Poppins', 'Segoe UI', Roboto, sans-serif;
            color: var(--primary-text);
            background: var(--primary-gradient);
            background-size: 400% 400%;
            animation: gradientBG 20s ease infinite;
            line-height: 1.6;
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Hide Streamlit Default Elements */
        #MainMenu, footer, header, .css-ch5dnh {
            visibility: hidden;
            display: none;
        }
        
        /* Remove extra bar */
        .css-1dp5vir, .css-1d391kg, .block-container {
            padding-top: 1rem !important;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            25% { background-position: 50% 100%; }
            50% { background-position: 100% 50%; }
            75% { background-position: 50% 0%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Glass Morphism Effects */
        .glass-effect {
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            border-radius: var(--rounded-md);
            box-shadow: var(--glass-shadow);
            transition: var(--transition-normal);
        }
        
        .glass-effect:hover {
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
            transform: translateY(-2px);
        }
        
        /* Modern Title with Enhanced Animation */
        .title {
            font-size: 3.8em;
            font-weight: 800;
            text-align: center;
            margin: 0.5em 0;
            background: var(--text-gradient);
            background-size: 300% 300%;
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: titleGradient 8s ease infinite, float 6s ease-in-out infinite;
            padding: 0.2em;
            text-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
            letter-spacing: 2px;
        }

        @keyframes titleGradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        /* Ultra Modern Search Box */
        .search-container {
            position: relative;
            margin: 30px 0;
            transform-style: preserve-3d;
            perspective: 500px;
        }
        
        .search-icon {
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: rgba(255, 255, 255, 0.7);
            font-size: 20px;
            z-index: 2;
            pointer-events: none;
            transition: var(--transition-normal);
        }
        
        .stTextInput {
            position: relative;
        }
        
        .stTextInput::before {
            content: '🔍';
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 20px;
            z-index: 10;
            color: rgba(255, 255, 255, 0.7);
        }
        
        .stTextInput input {
            width: 100%;
            padding: 18px 25px 18px 55px !important;
            margin: 12px 0;
            border-radius: var(--rounded-full);
            border: none;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.2), 0 10px 20px rgba(0, 0, 0, 0.15);
            color: white;
            font-size: 18px;
            font-weight: 500;
            transition: var(--transition-bounce);
            animation: searchEnter 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
            transform-origin: center;
        }
        
        @keyframes searchEnter {
            0% { transform: scale(0.8) translateY(20px); opacity: 0; }
            100% { transform: scale(1) translateY(0); opacity: 1; }
        }

        .stTextInput input:focus {
            background: rgba(255, 255, 255, 0.12);
            box-shadow: 0 0 30px rgba(131, 58, 180, 0.5), inset 0 0 15px rgba(0, 0, 0, 0.1);
            transform: translateY(-3px) scale(1.01);
            outline: none;
        }
        
        .stTextInput input::placeholder {
            color: rgba(255, 255, 255, 0.6);
            transition: var(--transition-normal);
        }
        
        .stTextInput input:focus::placeholder {
            opacity: 0.6;
            transform: translateX(10px);
        }
        
        /* Enhanced Navigation Menu */
        .nav-menu {
            display: flex;
            justify-content: center;
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            padding: 10px;
            border-radius: var(--rounded-md);
            margin-bottom: 20px;
            box-shadow: var(--glass-shadow);
            position: sticky;
            top: 0;
            z-index: 1000;
            border: 1px solid var(--glass-border);
        }
        
        .nav-item {
            color: white;
            padding: 10px 20px;
            margin: 0 5px;
            border-radius: var(--rounded-full);
            text-decoration: none;
            font-weight: 600;
            transition: var(--transition-normal);
            position: relative;
            overflow: hidden;
            cursor: pointer;
        }
        
        .nav-item:before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.1);
            transition: var(--transition-normal);
        }
        
        .nav-item:hover:before {
            left: 0;
        }
        
        .nav-item.active {
            background: var(--accent-gradient);
            background-size: 200% 200%;
            animation: gradientShift 3s ease infinite;
            box-shadow: var(--shadow-md);
        }
        
        .nav-item:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-md);
        }
        
        .nav-item .icon {
            margin-right: 8px;
        }
        
        /* Advanced Button Styles with Hover Effects */
        .custom-button {
            display: inline-block;
            padding: 14px 28px;
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 1px;
            color: #fff;
            background: var(--accent-gradient);
            background-size: 200% 200%;
            border: none;
            border-radius: var(--rounded-full);
            cursor: pointer;
            transition: var(--transition-normal);
            box-shadow: var(--shadow-md);
            position: relative;
            overflow: hidden;
            z-index: 1;
            margin: 10px 15px;
            text-transform: uppercase;
        }

        .custom-button:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--accent-gradient);
            background-size: 200% 200%;
            opacity: 0;
            transition: opacity 0.5s ease;
            z-index: -1;
            animation: gradientShift 3s ease infinite;
        }

        .custom-button:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: var(--shadow-lg);
        }

        .custom-button:hover:before {
            opacity: 1;
        }

        .custom-button:active {
            transform: translateY(2px);
            box-shadow: var(--shadow-sm);
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Modern Center Layout */
        .center-buttons {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            margin: 30px 0;
        }
        
        /* Cart and Favorites Counters */
        .counter-badge {
            position: absolute;
            top: -8px;
            right: -8px;
            background: #ff3860;
            color: white;
            border-radius: 50%;
            width: 22px;
            height: 22px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(255, 56, 96, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(255, 56, 96, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 56, 96, 0); }
        }

        /* Advanced Product Box with 3D Effects */
        .product-box {
            display: flex;
            flex-direction: column;
            border-radius: var(--rounded-lg);
            padding: 25px;
            margin-bottom: 30px;
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: var(--shadow-lg);
            transition: var(--transition-bounce);
            overflow: hidden;
            border: 1px solid var(--glass-border);
            position: relative;
            transform-style: preserve-3d;
            perspective: 1000px;
        }

        @media (min-width: 768px) {
            .product-box {
                flex-direction: row;
            }
        }

        .product-box:hover {
            transform: translateY(-10px) scale(1.02) rotateX(2deg);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            background: var(--card-hover-bg);
        }
        
        /* Product Actions */
        .product-actions {
            position: absolute;
            top: 15px;
            right: 15px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            z-index: 10;
        }
        
        .action-button {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(5px);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: var(--transition-normal);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            color: white;
            font-size: 18px;
            opacity: 0.8;
            transform: translateX(60px);
            animation: slideIn 0.3s forwards;
            animation-delay: calc(var(--i) * 0.1s);
        }
        
        @keyframes slideIn {
            to { transform: translateX(0); }
        }
        
        .action-button:hover {
            background: var(--accent-gradient);
            background-size: 200% 200%;
            animation: gradientShift 3s ease infinite;
            transform: translateY(-3px);
            opacity: 1;
        }
        
        .action-button.favorite.active {
            background: linear-gradient(45deg, #ff416c, #ff4b2b);
            color: white;
            animation: heartbeat 1.5s ease-in-out infinite;
        }
        
        @keyframes heartbeat {
            0% { transform: scale(1); }
            25% { transform: scale(1.2); }
            50% { transform: scale(1); }
            75% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }

        /* Advanced Animation for Product Box */
        @keyframes reveal {
            0% { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        .product-image {
            flex: 1;
            margin-right: 0;
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
            border-radius: var(--rounded-md);
            box-shadow: var(--shadow-md);
            animation: reveal 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            transform: translateZ(20px);
        }

        @media (min-width: 768px) {
            .product-image {
                margin-right: 25px;
                margin-bottom: 0;
            }
        }

        .product-image img {
            width: 100%;
            height: auto;
            border-radius: var(--rounded-md);
            transition: transform 0.8s cubic-bezier(0.165, 0.84, 0.44, 1);
            object-fit: cover;
        }

        .product-image:hover img {
            transform: scale(1.15) rotate(2deg);
        }

        .product-image::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(to top, rgba(0,0,0,0.5), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .product-image:hover::after {
            opacity: 1;
        }

        .product-info {
            flex: 3;
            animation: reveal 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.2s both;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transform: translateZ(30px);
        }

        .product-info h3 {
            margin: 0 0 15px 0;
            font-size: 1.8em;
            font-weight: 700;
            color: #fff;
            letter-spacing: 0.5px;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            background: linear-gradient(90deg, #fff, #f0f0f0);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .product-info p {
            font-size: 1.2em;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 20px;
            font-weight: 500;
        }

        .product-info p strong {
            color: var(--accent-color);
            font-weight: 600;
        }
        
        /* Price tag with animation */
        .price-tag {
            display: inline-block;
            background: linear-gradient(45deg, #00b09b, #96c93d);
            padding: 8px 15px;
            border-radius: var(--rounded-md);
            color: white;
            font-weight: bold;
            margin-bottom: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
            animation: priceFloat 3s ease-in-out infinite;
        }
        
        @keyframes priceFloat {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
        
        .price-tag:before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: 0.5s;
        }
        
        .price-tag:hover:before {
            left: 100%;
        }

        /* Modern Button with Animation */
        .ebay-link {
            display: inline-block;
            background: linear-gradient(45deg, #4158D0, #C850C0, #FFCC70);
            background-size: 200% 200%;
            color: white;
            padding: 14px 28px;
            border-radius: var(--rounded-full);
            text-decoration: none;
            font-weight: 600;
            letter-spacing: 1px;
            transition: var(--transition-normal);
            box-shadow: var(--shadow-md);
            position: relative;
            overflow: hidden;
            align-self: flex-start;
            animation: gradientShift 3s ease infinite;
            text-transform: uppercase;
            font-size: 14px;
        }

        .ebay-link:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
            background-position: right center;
        }

        .ebay-link:active {
            transform: translateY(2px);
            box-shadow: var(--shadow-sm);
        }

        .ebay-link::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: 0.5s;
        }

        .ebay-link:hover::before {
            left: 100%;
        }

        /* Modern Pagination Buttons */
        .pagination-btn {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: var(--rounded-full);
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition-normal);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            box-shadow: var(--shadow-md);
        }

        .pagination-btn:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-3px);
            box-shadow: var(--shadow-lg);
        }

        .pagination-btn:active {
            transform: translateY(0);
        }

        /* Modern loading animation */
        .stSpinner > div {
            border-color: var(--accent-color) transparent transparent transparent !important;
        }

        /* Divider styling */
        hr {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            border: none;
            margin: 30px 0;
        }

        /* Success message */
        .stSuccess {
            background: rgba(100, 255, 218, 0.1) !important;
            color: var(--accent-color) !important;
            border-radius: 10px !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(100, 255, 218, 0.2) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            animation: fadeInUp 0.5s ease-out;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Caption styling */
        .caption-text {
            font-size: 0.9em;
            text-align: center;
            color: var(--secondary-text);
            margin-top: 5px;
            font-style: italic;
        }

        /* Cart Panel */
        .cart-panel {
            position: fixed;
            top: 0;
            right: -400px;
            width: 400px;
            height: 100vh;
            background: var(--primary-gradient);
            background-size: 400% 400%;
            animation: gradientBG 20s ease infinite;
            z-index: 1000;
            box-shadow: -5px 0 30px rgba(0, 0, 0, 0.3);
            transition: right 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            padding: 20px;
            overflow-y: auto;
            border-left: 1px solid var(--glass-border);
        }
        
        .cart-panel.active {
            right: 0;
        }
        
        .cart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--glass-border);
        }
        
        .cart-header h2 {
            font-size: 1.8em;
            font-weight: 700;
            color: white;
        }
        
        .close-cart {
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            transition: var(--transition-normal);
        }
        
        .close-cart:hover {
            transform: rotate(90deg);
        }
        
        .cart-items {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .cart-item {
            display: flex;
            background: var(--glass-bg);
            border-radius: var(--rounded-md);
            overflow: hidden;
            box-shadow: var(--shadow-md);
            animation: fadeInUp 0.5s ease-out;
        }
        
        .cart-item-img {
            width: 80px;
            height: 80px;
            object-fit: cover;
        }
        
        .cart-item-details {
            flex: 1;
            padding: 10px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .cart-item-title {
            font-size: 1em;
            font-weight: 600;
            color: white;
            margin: 0;
        }
        
        .cart-item-price {
            color: var(--accent-color);
            font-weight: 600;
        }
        
        .cart-item-remove {
            background: none;
            border: none;
            color: #ff3860;
            cursor: pointer;
            transition: var(--transition-normal);
        }
        
        .cart-item-remove:hover {
            transform: scale(1.2);
        }
        
        .cart-total {
            margin-top: 20px;
            padding: 15px;
            background: var(--glass-bg);
            border-radius: var(--rounded-md);
            font-size: 1.2em;
            font-weight: 700;
            text-align: right;
        }
        
        .checkout-btn {
            display: block;
            width: 100%;
            padding: 15px;
            margin-top: 20px;
            background: var(--accent-gradient);
            background-size: 200% 200%;
            animation: gradientShift 3s ease infinite;
            border: none;
            border-radius: var(--rounded-md);
            color: white;
            font-size: 1.2em;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition-normal);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .checkout-btn:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-lg);
        }
        
        .checkout-btn:active {
            transform: translateY(0);
        }

        /* Make streamlit elements look modern */
        .stButton button {
            border-radius: var(--rounded-full) !important;
            border: none !important;
            padding: 0.6em 1.5em !important;
            font-weight: 600 !important;
            background: var(--accent-gradient) !important;
            background-size: 200% 200% !important;
            color: white !important;
            transition: var(--transition-normal) !important;
            box-shadow: var(--shadow-md) !important;
            animation: gradientShift 3s ease infinite !important;
        }

        .stButton button:hover {
            transform: translateY(-3px) !important;
            box-shadow: var(--shadow-lg) !important;
        }

        .stButton button:active {
            transform: translateY(0) !important;
            box-shadow: var(--shadow-sm) !important;
        }

        /* Image styling */
        .stImage img {
            border-radius: var(--rounded-lg);
            box-shadow: var(--shadow-lg);
            transition: all 0.5s ease;
        }

        .stImage img:hover {
            transform: scale(1.02);
        }

        /* Page indicator */
        .page-indicator {
            background: var(--glass-bg);
            padding: 8px 15px;
            border-radius: var(--rounded-full);
            font-size: 14px;
            color: white;
            margin: 0 auto;
            text-align: center;
            width: fit-content;
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            box-shadow: var(--shadow-sm);
        }

        /* No results message */
        .no-results {
            text-align: center;
            padding: 50px 0;
            color: var(--secondary-text);
            font-size: 1.5em;
            font-weight: 300;
            letter-spacing: 1px;
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(45deg, #833ab4, #fd1d1d);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(45deg, #fd1d1d, #833ab4);
        }
        
        /* Toast notification */
        .toast {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            padding: 15px 25px;
            border-radius: var(--rounded-md);
            color: white;
            font-weight: 600;
            box-shadow: var(--shadow-lg);
            z-index: 9999;
            display: flex;
            align-items: center;
            gap: 10px;
            animation: toastIn 0.5s ease-out forwards;
            border: 1px solid var(--glass-border);
            max-width: 350px;
        }
        
        @keyframes toastIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .toast.success {
            border-left: 5px solid #48c774;
        }
        
        .toast.error {
            border-left: 5px solid #ff3860;
        }
        
        .toast.info {
            border-left: 5px solid #3298dc;
        }
        
        .toast .icon {
            font-size: 24px;
        }
        
        .toast .close {
            margin-left: auto;
            background: none;
            border: none;
            color: white;
            font-size: 18px;
            cursor: pointer;
            opacity: 0.7;
            transition: var(--transition-normal);
        }
        
        .toast .close:hover {
            opacity: 1;
            transform: scale(1.1);
        }
        
        /* Favorites panel */
        .favorites-panel {
            position: fixed;
            top: 0;
            left: -400px;
            width: 400px;
            height: 100vh;
            background: var(--primary-gradient);
            background-size: 400% 400%;
            animation: gradientBG 20s ease infinite;
            z-index: 1000;
            box-shadow: 5px 0 30px rgba(0, 0, 0, 0.3);
            transition: left 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            padding: 20px;
            overflow-y: auto;
            border-right: 1px solid var(--glass-border);
        }
        
        .favorites-panel.active {
            left: 0;
        }
        
        .fav-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--glass-border);
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def fetch_html(url):
    headers = {
        "User-Agent": "Your User Agent",
        "Accept-Language": "en-US, en;q=0.5"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all("div", class_="s-item__info")
    images = soup.find_all("div", class_="s-item__image-wrapper image-treatment")
    
    items = []
    for product, img in zip(products, images):
        title = product.select_one('.s-item__title').text if product.select_one('.s-item__title') else "N/A"
        link = product.select_one('.s-item__link')['href'] if product.select_one('.s-item__link') else "N/A"
        price = product.select_one('.s-item__price').text if product.select_one('.s-item__price') else "N/A"
        img_tag = img.find("img")
        img_url = img_tag['src'] if img_tag else "N/A"
        items.append((link, title, price, img_url))
    return items

def store_data(database, data):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS products')  

    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                      link TEXT, 
                      title TEXT, 
                      price TEXT, 
                      img TEXT)''')

    data = data[2:]  
    if data:
        data = [data[0]] + data  
        cursor.executemany('INSERT INTO products (link, title, price, img) VALUES (?,?,?,?)', data)
    conn.commit()
    conn.close()

def fetch_product_data(database='products.db'):
    conn = sqlite3.connect(database)
    query = '''SELECT link, title, price, img FROM products'''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def extract_price(price_str):
    """
    Extract the minimum price from a price string (handles ranges like "166.95 to 198.95").
    """
    
    price_str = price_str.replace('$', '').replace(',', '')
    
    match = re.search(r'\d+\.\d+', price_str)
    if match:
        return float(match.group())
    return 0.0  

def sort_products(products, sort_option):
    """
    Sort products based on the selected option.
    """
    if sort_option == "The Cheapest":
        
        products['price_numeric'] = products['price'].apply(extract_price)
        products = products.sort_values(by='price_numeric', ascending=True)
    elif sort_option == "The Most Expensive":
        
        products['price_numeric'] = products['price'].apply(extract_price)
        products = products.sort_values(by='price_numeric', ascending=False)
    return products

def cleanup_database(database='products.db'):
    """
    Delete the database file when the script exits.
    """
    if os.path.exists(database):
        os.remove(database)
        print(f"Deleted database file: {database}")


atexit.register(cleanup_database)

def main():
    st.set_page_config(layout="wide", page_title="Modern Online Shop", page_icon="🛍️")
    apply_custom_css()  # Apply custom CSS
    
    # Initialize session state for cart and favorites
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    if 'cart_count' not in st.session_state:
        st.session_state.cart_count = 0
    if 'favorites_count' not in st.session_state:
        st.session_state.favorites_count = 0
    if 'show_toast' not in st.session_state:
        st.session_state.show_toast = False
    if 'toast_message' not in st.session_state:
        st.session_state.toast_message = ""
    if 'toast_type' not in st.session_state:
        st.session_state.toast_type = "success"
    
    # Modern title
    st.markdown('<div class="title">🛍️ Modern Online Shop 🛍️</div>', unsafe_allow_html=True)

    # Navigation menu
    st.markdown('''
        <div class="nav-menu">
            <div class="nav-item active"><span class="icon">🏠</span> Home</div>
            <div class="nav-item"><span class="icon">🔍</span> Explore</div>
            <div class="nav-item" onclick="showFavorites()"><span class="icon">❤️</span> Favorites 
                <span class="counter-badge">{}</span>
            </div>
            <div class="nav-item" onclick="showCart()"><span class="icon">🛒</span> Cart 
                <span class="counter-badge">{}</span>
            </div>
            <div class="nav-item"><span class="icon">👤</span> Account</div>
        </div>
    '''.format(st.session_state.favorites_count, st.session_state.cart_count), unsafe_allow_html=True)

    # Main image with responsive container
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", use_container_width=True)
        st.markdown('<p class="caption-text">🐍 Powered by Python 🐍</p>', unsafe_allow_html=True)

    # Search container with glass effect and modern search box
    st.markdown('<div class="glass-effect search-container" style="padding: 20px; margin: 20px 0;">', unsafe_allow_html=True)
    search_query = st.text_input("", value="", max_chars=None, placeholder='Search for products...', key='searchbox', help='Search in eBay 🔎')
    st.markdown('</div>', unsafe_allow_html=True)

    # Centered buttons under the search box
    st.markdown('<div class="center-buttons">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("The Cheapest", key="cheapest"):
            st.session_state.sort_option = "The Cheapest"
    with col2:
        if st.button("The Most Expensive", key="most_expensive"):
            st.session_state.sort_option = "The Most Expensive"
    with col3:
        if st.button("Most Popular", key="popular"):
            st.session_state.sort_option = "Most Popular"
    st.markdown('</div>', unsafe_allow_html=True)

    if search_query:
        with st.spinner("Fetching data from eBay...🔎"):
            base_url = "https://www.ebay.com/sch/i.html?_nkw="
            url = f"{base_url}{search_query}"
            html = fetch_html(url)
            products = parse_html(html)
            store_data('products.db', products)
            st.success("✅ Data fetched successfully ✅")
    
    try:
        products = fetch_product_data()
    except pd.io.sql.DatabaseError:
        products = pd.DataFrame(columns=['link', 'title', 'price', 'img']) 

    # Sort products based on the selected option
    sort_option = st.session_state.get('sort_option', "Default")
    if sort_option != "Default":
        products = sort_products(products, sort_option)

    # If no products found
    if products.empty:
        st.markdown('<div class="no-results">No products found. Try a different search!</div>', unsafe_allow_html=True)
    else:
        # Pagination
        items_per_page = 4
        total_pages = max((len(products) + items_per_page - 1) // items_per_page, 1)
        page_number = st.session_state.get('page_number', 1)

        # Page indicator
        st.markdown(f'<div class="page-indicator">Page {page_number} of {total_pages}</div>', unsafe_allow_html=True)

        start_idx = (page_number - 1) * items_per_page
        end_idx = start_idx + items_per_page
        
        # Product display with enhanced features
        for idx in range(start_idx, min(end_idx, len(products))):
            product = products.iloc[idx]
            product_id = idx
            
            # Check if product is in favorites
            is_favorite = any(fav.get('id') == product_id for fav in st.session_state.favorites)
            fav_class = "active" if is_favorite else ""
            
            # Check if product is in cart
            in_cart = any(item.get('id') == product_id for item in st.session_state.cart)
            cart_btn_text = "Added to Cart" if in_cart else "Add to Cart"
            
            st.markdown(f'''
                <div class="product-box">
                    <div class="product-actions">
                        <div class="action-button favorite {fav_class}" style="--i:1" onclick="toggleFavorite({product_id}, '{product['title']}', '{product['price']}', '{product['img']}', '{product['link']}')">
                            ❤️
                        </div>
                        <div class="action-button" style="--i:2" onclick="addToCart({product_id}, '{product['title']}', '{product['price']}', '{product['img']}', '{product['link']}')">
                            🛒
                        </div>
                        <div class="action-button" style="--i:3">
                            🔍
                        </div>
                    </div>
                    <div class="product-image">
                        <img src="{product['img']}" width="100%">
                    </div>
                    <div class="product-info">
                        <h3>{product['title']}</h3>
                        <div class="price-tag">{product['price']}</div>
                        <p><strong>Condition:</strong> New</p>
                        <p><strong>Shipping:</strong> Free shipping</p>
                        <div style="display: flex; gap: 15px; margin-top: 10px;">
                            <a target="_blank" href="{product['link']}" class="ebay-link">View on eBay</a>
                            <button class="ebay-link" style="border: none; cursor: pointer;" 
                                onclick="addToCart({product_id}, '{product['title']}', '{product['price']}', '{product['img']}', '{product['link']}')">
                                {cart_btn_text}
                            </button>
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

        # Pagination controls
        st.markdown('<div class="center-buttons">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if page_number > 1:
                if st.button("◀ Previous", key="prev"):
                    st.session_state.page_number = page_number - 1
        
        with col2:
            st.markdown(f'<div style="text-align: center; margin-top: 10px;">Page {page_number} of {total_pages}</div>', unsafe_allow_html=True)
            
        with col3:
            if page_number < total_pages:
                if st.button("Next ▶", key="next"):
                    st.session_state.page_number = page_number + 1
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Cart Panel HTML
    cart_items_html = ""
    cart_total = 0
    
    for item in st.session_state.cart:
        price_value = extract_price(item.get('price', '0'))
        cart_total += price_value
        cart_items_html += f'''
            <div class="cart-item">
                <img class="cart-item-img" src="{item.get('img', '')}" alt="{item.get('title', 'Product')}">
                <div class="cart-item-details">
                    <h4 class="cart-item-title">{item.get('title', 'Product')}</h4>
                    <div class="cart-item-price">{item.get('price', '$0.00')}</div>
                    <button class="cart-item-remove" onclick="removeFromCart({item.get('id', 0)})">Remove</button>
                </div>
            </div>
        '''
    
    # Cart panel
    st.markdown(f'''
        <div class="cart-panel" id="cartPanel">
            <div class="cart-header">
                <h2>Your Cart ({st.session_state.cart_count})</h2>
                <button class="close-cart" onclick="hideCart()">×</button>
            </div>
            <div class="cart-items">
                {cart_items_html if st.session_state.cart else "<p>Your cart is empty</p>"}
            </div>
            <div class="cart-total">
                Total: ${cart_total:.2f}
            </div>
            <button class="checkout-btn">Proceed to Checkout</button>
        </div>
    ''', unsafe_allow_html=True)
    
    # Favorites Panel HTML
    fav_items_html = ""
    
    for item in st.session_state.favorites:
        fav_items_html += f'''
            <div class="cart-item">
                <img class="cart-item-img" src="{item.get('img', '')}" alt="{item.get('title', 'Product')}">
                <div class="cart-item-details">
                    <h4 class="cart-item-title">{item.get('title', 'Product')}</h4>
                    <div class="cart-item-price">{item.get('price', '$0.00')}</div>
                    <button class="cart-item-remove" onclick="removeFromFavorites({item.get('id', 0)})">Remove</button>
                </div>
            </div>
        '''
    
    # Favorites panel
    st.markdown(f'''
        <div class="favorites-panel" id="favoritesPanel">
            <div class="fav-header">
                <h2>Your Favorites ({st.session_state.favorites_count})</h2>
                <button class="close-cart" onclick="hideFavorites()">×</button>
            </div>
            <div class="cart-items">
                {fav_items_html if st.session_state.favorites else "<p>You have no favorites yet</p>"}
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Toast notification
    if st.session_state.show_toast:
        icon = "✅" if st.session_state.toast_type == "success" else "❌" if st.session_state.toast_type == "error" else "ℹ️"
        st.markdown(f'''
            <div class="toast {st.session_state.toast_type}">
                <span class="icon">{icon}</span>
                <span>{st.session_state.toast_message}</span>
                <button class="close" onclick="hideToast()">×</button>
            </div>
        ''', unsafe_allow_html=True)
        st.session_state.show_toast = False
    
    # JavaScript for interactive functionality
    st.markdown('''
        <script>
            function showCart() {
                document.getElementById('cartPanel').classList.add('active');
            }
            
            function hideCart() {
                document.getElementById('cartPanel').classList.remove('active');
            }
            
            function showFavorites() {
                document.getElementById('favoritesPanel').classList.add('active');
            }
            
            function hideFavorites() {
                document.getElementById('favoritesPanel').classList.remove('active');
            }
            
            function addToCart(id, title, price, img, link) {
                window.parent.postMessage({
                    type: 'streamlit:addToCart',
                    id: id,
                    title: title,
                    price: price,
                    img: img,
                    link: link
                }, '*');
            }
            
            function removeFromCart(id) {
                window.parent.postMessage({
                    type: 'streamlit:removeFromCart',
                    id: id
                }, '*');
            }
            
            function toggleFavorite(id, title, price, img, link) {
                window.parent.postMessage({
                    type: 'streamlit:toggleFavorite',
                    id: id,
                    title: title,
                    price: price,
                    img: img,
                    link: link
                }, '*');
            }
            
            function removeFromFavorites(id) {
                window.parent.postMessage({
                    type: 'streamlit:removeFromFavorites',
                    id: id
                }, '*');
            }
            
            function hideToast() {
                const toast = document.querySelector('.toast');
                if (toast) {
                    toast.style.animation = 'toastOut 0.5s forwards';
                    setTimeout(() => {
                        toast.remove();
                    }, 500);
                }
            }
            
            // Auto hide toast after 5 seconds
            setTimeout(hideToast, 5000);
        </script>
    ''', unsafe_allow_html=True)

# Add these functions to handle cart and favorites
def handle_add_to_cart(id, title, price, img, link):
    """Add item to cart"""
    # Check if already in cart
    if not any(item.get('id') == id for item in st.session_state.cart):
        st.session_state.cart.append({
            'id': id,
            'title': title,
            'price': price,
            'img': img,
            'link': link
        })
        st.session_state.cart_count = len(st.session_state.cart)
        st.session_state.show_toast = True
        st.session_state.toast_message = "Item added to cart"
        st.session_state.toast_type = "success"
    else:
        st.session_state.show_toast = True
        st.session_state.toast_message = "Item already in cart"
        st.session_state.toast_type = "info"

def handle_remove_from_cart(id):
    """Remove item from cart"""
    st.session_state.cart = [item for item in st.session_state.cart if item.get('id') != id]
    st.session_state.cart_count = len(st.session_state.cart)
    st.session_state.show_toast = True
    st.session_state.toast_message = "Item removed from cart"
    st.session_state.toast_type = "info"

def handle_toggle_favorite(id, title, price, img, link):
    """Toggle item in favorites"""
    if any(item.get('id') == id for item in st.session_state.favorites):
        st.session_state.favorites = [item for item in st.session_state.favorites if item.get('id') != id]
        st.session_state.show_toast = True
        st.session_state.toast_message = "Removed from favorites"
        st.session_state.toast_type = "info"
    else:
        st.session_state.favorites.append({
            'id': id,
            'title': title,
            'price': price,
            'img': img,
            'link': link
        })
        st.session_state.show_toast = True
        st.session_state.toast_message = "Added to favorites"
        st.session_state.toast_type = "success"
    st.session_state.favorites_count = len(st.session_state.favorites)

def handle_remove_from_favorites(id):
    """Remove item from favorites"""
    st.session_state.favorites = [item for item in st.session_state.favorites if item.get('id') != id]
    st.session_state.favorites_count = len(st.session_state.favorites)
    st.session_state.show_toast = True
    st.session_state.toast_message = "Removed from favorites"
    st.session_state.toast_type = "info"

if __name__ == "__main__":
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1
    if 'sort_option' not in st.session_state:
        st.session_state.sort_option = "Default"
    
    # Handle messages from frontend
    message = st.query_params.get("streamlitMessage", None)
    if message:
        message_type = message[0]
        if message_type == "addToCart":
            id = int(st.query_params.get("id", [0])[0])
            title = st.query_params.get("title", [""])[0]
            price = st.query_params.get("price", ["$0.00"])[0]
            img = st.query_params.get("img", [""])[0]
            link = st.query_params.get("link", [""])[0]
            handle_add_to_cart(id, title, price, img, link)
        
        elif message_type == "removeFromCart":
            id = int(st.query_params.get("id", [0])[0])
            handle_remove_from_cart(id)
        
        elif message_type == "toggleFavorite":
            id = int(st.query_params.get("id", [0])[0])
            title = st.query_params.get("title", [""])[0]
            price = st.query_params.get("price", ["$0.00"])[0]
            img = st.query_params.get("img", [""])[0]
            link = st.query_params.get("link", [""])[0]
            handle_toggle_favorite(id, title, price, img, link)
        
        elif message_type == "removeFromFavorites":
            id = int(st.query_params.get("id", [0])[0])
            handle_remove_from_favorites(id)
    
    main()
