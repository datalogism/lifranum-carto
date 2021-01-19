<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xi="http://www.w3.org/2001/XInclude"
    exclude-result-prefixes="xs"
    version="2.0"
    xmlns:tei="http://www.tei-c.org/ns/1.0">
    
    <xsl:output method="text"/> <!-- pour faire une sortie en csv -->
    
    <xsl:template match="/">
        <xsl:text>Nom Prenom/types de distinctions/description &#x0a;</xsl:text>
        <xsl:for-each select="//div[@source='ile_en_ile']">
            <xsl:for-each select="./list[@subtype='distinctions littéraires']">
                <xsl:for-each select="./item">
                        <xsl:value-of select="concat(ancestor::div/@ana,'/',parent::list/@subtype,'/',.,'&#xA;')"/>
                </xsl:for-each>
            </xsl:for-each>
            <xsl:for-each select="./list[@subtype='distinctions et prix littéraires']">
                <xsl:for-each select="./item">
                    <xsl:value-of select="concat(ancestor::div/@ana,'/',parent::list/@subtype,'/',.,'&#xA;')"/>
                </xsl:for-each>
            </xsl:for-each>
            <xsl:for-each select="./list[@subtype='distinctions']">
                <xsl:for-each select="./item">
                    <xsl:value-of select="concat(ancestor::div/@ana,'/',parent::list/@subtype,'/',.,'&#xA;')"/>
                </xsl:for-each>
            </xsl:for-each>
            <xsl:for-each select="./list[@subtype='distinction littéraire']">
                <xsl:for-each select="./item">
                    <xsl:value-of select="concat(ancestor::div/@ana,'/',parent::list/@subtype,'/',.,'&#xA;')"/>
                </xsl:for-each>
            </xsl:for-each>
            <xsl:for-each select="./list[@subtype='distinctions, invitations et interventions publiques']">
                <xsl:for-each select="./item">
                    <xsl:value-of select="concat(ancestor::div/@ana,'/',parent::list/@subtype,'/',.,'&#xA;')"/>
                </xsl:for-each>
            </xsl:for-each>
            <xsl:for-each select="./list[@subtype='prix et distinctions']">
                <xsl:for-each select="./item">
                    <xsl:value-of select="concat(ancestor::div/@ana,'/',parent::list/@subtype,'/',.,'&#xA;')"/>
                </xsl:for-each>
            </xsl:for-each>
            <xsl:for-each select="./list[@subtype='prix et distinctions littéraires']">
                <xsl:for-each select="./item">
                    <xsl:value-of select="concat(ancestor::div/@ana,'/',parent::list/@subtype,'/',.,'&#xA;')"/>
                </xsl:for-each>
            </xsl:for-each>
            <xsl:for-each select="./list[@subtype='prix et distinctions littéraires et au cinéma']">
                <xsl:for-each select="./item">
                    <xsl:value-of select="concat(ancestor::div/@ana,'/',parent::list/@subtype,'/',.,'&#xA;')"/>
                </xsl:for-each>
            </xsl:for-each>
            <xsl:for-each select="./list[@subtype='prix et distinctions sélectionnés']">
                <xsl:for-each select="./item">
                    <xsl:value-of select="concat(ancestor::div/@ana,'/',parent::list/@subtype,'/',.,'&#xA;')"/>
                </xsl:for-each>
            </xsl:for-each>
            <xsl:for-each select="./list[@subtype='prix littéraire']">
                <xsl:for-each select="./item">
                    <xsl:value-of select="concat(ancestor::div/@ana,'/',parent::list/@subtype,'/',.,'&#xA;')"/>
                </xsl:for-each>
            </xsl:for-each>
            
        </xsl:for-each>
    </xsl:template>
    
</xsl:stylesheet>
