package org.vacnar.prestamosgotaagota

interface Platform {
    val name: String
}

expect fun getPlatform(): Platform