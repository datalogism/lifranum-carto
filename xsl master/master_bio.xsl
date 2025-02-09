<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xi="http://www.w3.org/2001/XInclude"
    exclude-result-prefixes="xs"
    version="2.0"
    xmlns:tei="http://www.tei-c.org/ns/1.0">
    
    <xsl:output method="text"/> <!-- pour faire une sortie en csv -->
    
    <xsl:template match="/">
        <xsl:text>Nom Prenom/auteur bio/source &#x0a;</xsl:text>
        <xsl:for-each select="//div[@n='2']">
            <xsl:for-each select="./text">
                        <xsl:value-of select="concat(@ana,'/',@hand,'/',@source,'&#xA;')"/>
            </xsl:for-each>
        </xsl:for-each>
    </xsl:template>
    
</xsl:stylesheet>
