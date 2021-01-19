<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet  
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="2.0">
    
    <xsl:output method="text" indent="yes"/>
    

    <xsl:template match="/">
        <xsl:text>Catégorie dans la bibliographie île en île</xsl:text>
        <xsl:for-each select="distinct-values(//p)">
            <xsl:text>&#x0a;</xsl:text>
            <p><xsl:value-of select="."/></p>
        </xsl:for-each>
    </xsl:template>
    
</xsl:stylesheet>