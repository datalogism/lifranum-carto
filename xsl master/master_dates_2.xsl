<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xi="http://www.w3.org/2001/XInclude"
    exclude-result-prefixes="xs"
    version="2.0"
    xmlns:tei="http://www.tei-c.org/ns/1.0">
    
    <xsl:output method="text"/> <!-- pour faire une sortie en csv -->
    
    <xsl:template match="/">
        <xsl:text>Nom Prénom/ année de naissance/ source année de naissance / année de mort (île en île) / année de mort (viaf) &#x0a;</xsl:text>
        <xsl:for-each select="//div[@n='1']">
            <xsl:for-each select="./person">
               
                <xsl:value-of select="concat(./persName,'/',./birth/date,'/',./birth/@source,'/',./death[@source='ile_en_ile_auto']/date,'/',./death[@source='viaf']/date,'/','&#xA;')"/>
                
            </xsl:for-each>
        </xsl:for-each>
    </xsl:template>
    
</xsl:stylesheet>